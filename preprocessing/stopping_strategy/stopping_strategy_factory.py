from .offset_stopping_strategy import OffsetStoppingStrategy
from .fibonacci_stopping_strategy import FibonacciStoppingStrategy
from .stopping_strategy import StoppingStrategy


STOPPING_STRATEGIES = {'offset': OffsetStoppingStrategy, 'fib': FibonacciStoppingStrategy}


class StoppingStrategyFactory:

    @staticmethod
    def get(strategy: str, **kwargs) -> StoppingStrategy:
        try:
            return STOPPING_STRATEGIES[strategy](**kwargs)
        except Exception:
            print('Unable to instantiate StoppingStrategy [{}] with parameters: {}'.format(strategy, **kwargs))
            raise