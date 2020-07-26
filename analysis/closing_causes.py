from enum import Enum

class ClosingCauses(Enum):
    STOP_PROFIT = 'profit'
    STOP_LOSS = 'loss'
    REVERSE_SIGNAL = 'reverse'