from shared.columns import PreprocessingColumns
import pandas as pd
import numpy as np


PIPS_SCALING = 1/10000


def find_signals(ma_df: pd.DataFrame, tolerance: int) -> pd.DataFrame:
    pips_tolerance = tolerance * PIPS_SCALING
    short_avg = ma_df[PreprocessingColumns.SHORT_AVG]
    buy_threshold = ma_df[PreprocessingColumns.LONG_AVG] + pips_tolerance
    sell_threshold = ma_df[PreprocessingColumns.LONG_AVG] - pips_tolerance

    levels = hysteresis_levels(short_avg.to_numpy(), sell_threshold.to_numpy(), buy_threshold.to_numpy())
    level_changes = levels.astype(int).diff()
    buy_signals = find_buy_signals(ma_df, level_changes)
    sell_signals = find_sell_signals(ma_df, level_changes)
    signals = pd.merge(buy_signals, sell_signals, on=PreprocessingColumns.TIME, how='outer').fillna(False).sort_values(by=PreprocessingColumns.TIME)
    return signals[[PreprocessingColumns.TIME, PreprocessingColumns.BUY, PreprocessingColumns.SELL]].reset_index(drop=True)


# https://stackoverflow.com/questions/23289976/how-to-find-zero-crossings-with-hysteresis
def hysteresis_levels(data: np.array, lower: np.array, upper: np.array, initial = False) -> pd.Series:
    above = data >= upper
    between = (data <= lower) | above
    ind = np.nonzero(between)[0]
    if not ind.size:
        return np.zeros_like(data, dtype=bool) | initial
    cnt = np.cumsum(between)
    return pd.Series(np.where(cnt, above[ind[cnt-1]], initial))


def find_buy_signals(ma_df: pd.DataFrame, level_changes: pd.Series) -> pd.DataFrame:
    buy_signals = ma_df[level_changes == 1]
    buy_signals.insert(1, PreprocessingColumns.BUY, True)
    return buy_signals


def find_sell_signals(ma_df: pd.DataFrame, level_changes: pd.Series) -> pd.DataFrame:
    sell_signals = ma_df[level_changes == -1]
    sell_signals.insert(1, PreprocessingColumns.SELL, True)
    return sell_signals