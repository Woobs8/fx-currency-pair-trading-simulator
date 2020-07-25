from preprocessing.moving_average.moving_average import MovingAverage
from preprocessing.moving_average.exponential_moving_average import ExponentialMovingAverage
from preprocessing.moving_average.simple_moving_average import SimpleMovingAverage


MOVING_AVERAGES = {'sma':SimpleMovingAverage, 'ema':ExponentialMovingAverage}


class MovingAverageFactory:

    @staticmethod
    def get(fnc: str, **kwargs) -> MovingAverage:
        try:
            return MOVING_AVERAGES[fnc](**kwargs)
        except Exception:
            print('Unable to instantiate MovingAverage [{}] with parameters: {}'.format(fnc, **kwargs))
            raise