import pandas as pd


def sma(data: pd.Series, window: int) -> pd.Series:
    return data.rolling(window=window).mean()


def ema(data: pd.Series, window: int) -> pd.Series:
    return data.ewm(span=window, adjust=False).mean()
