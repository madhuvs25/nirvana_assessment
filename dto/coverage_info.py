from typing import Optional


class CoverageInfo:
    oop_max: Optional[float]
    remaining_oop_max: Optional[float]
    copay: Optional[float]

    def __init__(self, oop_max, remaining_oop_max, copay):
        self.oop_max = float(oop_max) if oop_max else None
        self.remaining_oop_max = float(remaining_oop_max) if remaining_oop_max else None
        self.copay = float(copay) if copay else None
