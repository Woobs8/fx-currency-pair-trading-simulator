from preprocessing.moving_average.moving_average_factory import MovingAverageFactory
from shared.columns import MovingAverageColumns
import pandas as pd


def calc_moving_averages(data: pd.Series, fnc: str, short_window: int, long_window: int) -> pd.DataFrame:
        short_ma = calc_moving_average(data, fnc, short_window).rename(MovingAverageColumns.SHORT_AVG)
        long_ma = calc_moving_average(data, fnc, long_window).rename(MovingAverageColumns.LONG_AVG)
        moving_averages = pd.merge(short_ma, long_ma, left_index=True, right_index=True)
        return moving_averages


def calc_moving_average(data: pd.Series, fnc: str, window: int) -> pd.Series:
    mavg = MovingAverageFactory.get(fnc, window=window)
    x = mavg.calc(data)
    return mavg.calc(data)