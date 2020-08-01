import pandas as pd
from datetime import datetime
from shared import ResolvedSignalColumns


def filter_between_years(signals: pd.DataFrame, start: datetime = None, stop: datetime = None, col: str = None) -> pd.DataFrame:
    if col is not None:
        if start is not None:
            signals = signals[signals[col] >= start]
        if stop is not None:
            signals = signals[signals[col] <= stop]
    else:
        if start is not None:
            signals = signals[signals.index >= start]
        if stop is not None:
            signals = signals[signals.index <= stop]
    return signals