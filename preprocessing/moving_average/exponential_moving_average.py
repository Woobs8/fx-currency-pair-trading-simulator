from .moving_average_function import MovingAverageFunction
import pandas as pd


class ExponentialMovingAverage(MovingAverageFunction):

    def calc(self, data: pd.Series) -> pd.Series:
        return data.ewm(span=self.window, adjust=False).mean()


    def __repr__(self):
        return "ema{}".format(self.window)


    def __str__(self):
        return "ema{}".format(self.window)
