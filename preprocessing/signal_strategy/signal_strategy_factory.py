from .moving_average_signal_strategy import MovingAverageSignalStrategy
from .signal_strategy import SignalStrategy
from ..moving_average.moving_average_factory import MovingAverageFactory


SIGNAL_STRATEGIES = {'ma':MovingAverageSignalStrategy}


class SignalStrategyFactory:

    @staticmethod
    def get(strategy: str, **kwargs) -> SignalStrategy:
        try:
            return SIGNAL_STRATEGIES[strategy](**kwargs)
        except Exception:
            print('Unable to instantiate SignalStrategy [{}] with parameters: {}'.format(strategy, **kwargs))
            raise