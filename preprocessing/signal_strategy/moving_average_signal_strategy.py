from preprocessing.signal_strategy.signal_strategy import SignalStrategy
from preprocessing.moving_average.moving_average import MovingAverage
from preprocessing.moving_average.moving_average_factory import MovingAverageFactory
from shared.columns import SourceDataColumns, MovingAverageColumns, SignalColumns
import pandas as pd
import numpy as np


class MovingAverageSignalStrategy(SignalStrategy):

    PIPS_SCALING = 1/10000


    def __init__(self, avg_fnc: str, short_window: int, long_window: int, quote: str, hysteresis: int):
        self.short_avg = MovingAverageFactory.get(avg_fnc, window=short_window)
        self.long_avg = MovingAverageFactory.get(avg_fnc, window=long_window)
        self.quote = quote
        self.hysteresis = hysteresis
        self.hyst_delta_pips = hysteresis * self.PIPS_SCALING


    def find_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        moving_averages = self.get_moving_averages(data, self.quote)
        short_avg = moving_averages[MovingAverageColumns.SHORT_AVG]
        buy_threshold = moving_averages[MovingAverageColumns.LONG_AVG] + self.hyst_delta_pips
        sell_threshold = moving_averages[MovingAverageColumns.LONG_AVG] - self.hyst_delta_pips
        levels = self.hysteresis_levels(short_avg.to_numpy(), sell_threshold.to_numpy(), buy_threshold.to_numpy())
        level_changes = levels.astype(int).diff()
        buy_signals = self.find_buy_signals(moving_averages, level_changes)
        sell_signals = self.find_sell_signals(moving_averages, level_changes)
        signals = pd.merge(buy_signals, sell_signals, left_index=True, right_index=True, how='outer').fillna(False)
        return signals


    def get_moving_averages(self, data: pd.DataFrame, quote: str) -> pd.DataFrame:
        short_ma = self.short_avg.calc(data[quote]).rename(MovingAverageColumns.SHORT_AVG)
        long_ma = self.long_avg.calc(data[quote]).rename(MovingAverageColumns.LONG_AVG)
        moving_averages = pd.merge(short_ma, long_ma, left_index=True, right_index=True)
        return moving_averages


    # https://stackoverflow.com/questions/23289976/how-to-find-zero-crossings-with-hysteresis
    def hysteresis_levels(self, data: np.array, lower: np.array, upper: np.array, initial = False) -> pd.Series:
        above = data >= upper
        between = (data <= lower) | above
        ind = np.nonzero(between)[0]
        if not ind.size:
            return np.zeros_like(data, dtype=bool) | initial
        cnt = np.cumsum(between)
        return pd.Series(np.where(cnt, above[ind[cnt-1]], initial))


    def find_buy_signals(self, ma: pd.DataFrame, level_changes: pd.Series) -> pd.Series:
        buy_signals = ma[(level_changes == 1).values]
        buy_signals.insert(1, SignalColumns.BUY, True)
        return buy_signals[SignalColumns.BUY]


    def find_sell_signals(self, ma: pd.DataFrame, level_changes: pd.Series) -> pd.Series:
        sell_signals = ma[(level_changes == -1).values]
        sell_signals.insert(1, SignalColumns.SELL, True)
        return sell_signals[SignalColumns.SELL]


    def __repr__(self):
        return "ma_{}_{}_{}_{}".format(self.short_avg, self.long_avg, self.quote, self.hysteresis)


    def __str__(self):
        return "ma_{}_{}_{}_{}".format(self.short_avg, self.long_avg, self.quote, self.hysteresis)