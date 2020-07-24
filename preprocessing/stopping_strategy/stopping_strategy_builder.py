from preprocessing.stopping_strategy.offset_stopping_strategy import OffsetStoppingStrategy
from preprocessing.stopping_strategy.stopping_strategy import StoppingStrategy


class StoppingStrategyBuilder:

    @staticmethod
    def get_strategy(strategy: str, stop_profit: int = None, stop_loss: int = None, lookback: int = None) -> StoppingStrategy:
        if strategy is 'offset':
            return OffsetStoppingStrategy(stop_profit, stop_loss, lookback)
        else:
            return OffsetStoppingStrategy(stop_profit, stop_loss, lookback)