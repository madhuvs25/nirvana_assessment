import json
from collections import namedtuple
from unittest.mock import patch, Mock

import pytest

from service.coverage_service import CoverageService

# Create a namedtuple for mock response data
MockResponseData = namedtuple('MockResponseData', ['oop_max', 'remaining_oop_max', 'copay'])

# Mock response data
mock_responses = [
    MockResponseData(7000, 9000, 1000),
    MockResponseData(20000, 6000, 50000),
    MockResponseData(10000, 8000, 2000)
]


# Helper function to create a mock response object
def create_mock_response(data, status_code=200):
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = {
        'oop_max': data.oop_max,
        'remaining_oop_max': data.remaining_oop_max,
        'copay': data.copay
    }
    return mock_response


# Patch the requests.get method
@patch('requests.get')
def test_calculate_coverage(mock_get):
    # Setup mock responses
    mock_get.side_effect = [create_mock_response(data) for data in mock_responses]

    # Initialize CoverageService
    service = CoverageService()

    # Call the method under test
    member_id = '1'
    coalesced_coverage = service.calculate_coverage(member_id, coalesce_strategy=None)

    # Assert the coalesced coverage info
    assert coalesced_coverage.oop_max == 20000
    assert coalesced_coverage.remaining_oop_max == 9000
    assert coalesced_coverage.copay == 2000


if __name__ == "__main__":
    pytest.main()
