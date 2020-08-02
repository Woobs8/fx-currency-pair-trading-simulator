from .moving_average_function import MovingAverageFunction
import pandas as pd

class SimpleMovingAverage(MovingAverageFunction):

    def calc(self, data: pd.DataFrame) -> pd.Series:
        return data.rolling(window=window).mean()


    def __repr__(self):
        return "(window:{})".format(self.window)


    def __str__(self):
        return "SimpleMovingAverage(window={})".format(self.window)
