from enum import IntEnum

class ClosingCauses(IntEnum):
    STOP_PROFIT = 1
    STOP_LOSS = 2
    REVERSE_SIGNAL = 3