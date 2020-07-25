from preprocessing.moving_average.moving_average import MovingAverage
import pandas as pd

class SimpleMovingAverage(MovingAverage):

    def calc(self, data: pd.DataFrame) -> pd.Series:
        return data.rolling(window=window).mean()


    def __repr__(self):
        return "sma{}".format(self.window)


    def __str__(self):
        return "sma{}".format(self.window)
