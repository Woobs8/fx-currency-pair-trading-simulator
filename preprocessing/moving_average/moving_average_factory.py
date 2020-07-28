from .moving_average_function import MovingAverageFunction
from .exponential_moving_average import ExponentialMovingAverage
from .simple_moving_average import SimpleMovingAverage


MOVING_AVERAGES = {'sma':SimpleMovingAverage, 'ema':ExponentialMovingAverage}


class MovingAverageFactory:

    @staticmethod
    def get(fnc: str, **kwargs) -> MovingAverageFunction:
        try:
            return MOVING_AVERAGES[fnc](**kwargs)
        except Exception:
            print('Unable to instantiate MovingAverage [{}] with parameters: {}'.format(fnc, **kwargs))
            raise