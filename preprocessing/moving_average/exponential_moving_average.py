from preprocessing.moving_average.moving_average import MovingAverage
import pandas as pd

class ExponentialMovingAverage(MovingAverage):

    def calc(self, data: pd.Series) -> pd.Series:
        return data.ewm(span=self.window, adjust=False).mean()


    def __repr__(self):
        return "ema{}".format(self.window)


    def __str__(self):
        return "ema{}".format(self.window)
