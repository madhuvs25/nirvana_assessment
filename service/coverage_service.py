from collections import Counter
from typing import List, Dict, Optional

from dto.coverage_info import CoverageInfo
import requests


class CoverageService:
    coverage_details: List[CoverageInfo] = []
    patient_coverage_details: Dict[str, List[CoverageInfo]] = {}

    def __init__(self):
        self.apis: List[str] = ['https://api1.com', 'https://api2.com',
                                'https://api3.com']

    def calculate_coverage(self, member_id: str, coalesce_strategy: Optional[str]) -> CoverageInfo:
        #fetch the coverage info from the individual APIs
        for api in self.apis:
            coverage_info: CoverageInfo = self.__fetch_coverage_info(member_id, api)
            if coverage_info:
                CoverageService.coverage_details.append(coverage_info)

        CoverageService.patient_coverage_details[member_id] = CoverageService.coverage_details
        #  coalesce the data fetch from the different API
        coalesced_coverage = self.__coalesce_coverage_info(CoverageService.coverage_details, coalesce_strategy)
        return coalesced_coverage

    def __fetch_coverage_info(self, member_id: str, api: str) -> Optional[CoverageInfo]:
        try:
            url: str = api + '?member_id=' + member_id
            response = requests.get(url)
            if response.status_code == 200:
                # Parse the JSON data
                data = response.json()
                if data:
                    return CoverageInfo(data['oop_max'], data['remaining_oop_max'], data['copay'])
        except Exception as e:
            print("Exception occurred during API call " + str(e))
            raise e
        return None

    def __coalesce_coverage_info(self, coverage_details: List[CoverageInfo],
                                 coalesce_strategy: Optional[str]) -> CoverageInfo:
        attributes = [obj.oop_max for obj in coverage_details if obj.oop_max > 0]
        oop_max = self.__get_individual_data_point(attributes, coalesce_strategy)
        attributes = [obj.remaining_oop_max for obj in coverage_details if 0 <= obj.remaining_oop_max <= oop_max]
        remaining_oop_max = self.__get_individual_data_point(attributes, coalesce_strategy)
        attributes = [obj.copay for obj in coverage_details if 0 < obj.copay <= oop_max]
        copay = self.__get_individual_data_point(attributes, coalesce_strategy)
        return CoverageInfo(oop_max, remaining_oop_max, copay)

    def __get_individual_data_point(self, attributes: List[float], coalesce_strategy: Optional[str]) -> float:
        if not coalesce_strategy :
            counter = Counter(attributes)
            most_common_element = counter.most_common()
            return_val: float = None
            for element in most_common_element:
                if element[0] > 0:
                    if element[1] > 1:
                        return_val = element[0]
                        break
                    elif element[1] == 1:
                        return_val = sum(attributes) / len(attributes)
                        break
            return return_val
        else:
            if attributes and coalesce_strategy == 'min':
                return min(attributes)
            elif  attributes and coalesce_strategy == 'max':
                return max(attributes)
            elif  attributes and coalesce_strategy == 'mean':
                return sum(attributes) / len(attributes)
        return None
