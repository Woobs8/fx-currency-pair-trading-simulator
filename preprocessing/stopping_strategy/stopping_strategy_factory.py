from .offset_stopping_strategy import OffsetStoppingStrategy
from .stopping_strategy import StoppingStrategy


STOPPING_STRATEGIES = {'offset':OffsetStoppingStrategy}


class StoppingStrategyFactory:

    @staticmethod
    def get(strategy: str, **kwargs) -> StoppingStrategy:
        try:
            return STOPPING_STRATEGIES[strategy](**kwargs)
        except Exception:
            print('Unable to instantiate StoppingStrategy [{}] with parameters: {}'.format(strategy, **kwargs))
            raise