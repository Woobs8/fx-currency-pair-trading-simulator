import pandas as pd
from shared import SourceDataColumns

TICK_PERIOD = {'min':'min', 'hour': 'H', 'day': 'D'}


def resample_source(data: pd.DataFrame, period: str) -> pd.DataFrame:
    try:
        period = TICK_PERIOD[period]
        return data.groupby(data.index.floor(period)).apply(find_quotes)
    except KeyError:
        raise RuntimeError('Invalid resampling period. Supported periods are [{}]'.format(','.join(TICK_PERIOD.keys())))
        
    
def find_quotes(period) -> pd.Series:
    entry = []
    entry.append(period.iloc[0, :][SourceDataColumns.QUOTE_OPEN])
    entry.append(period[SourceDataColumns.QUOTE_HIGH].max())
    entry.append(period[SourceDataColumns.QUOTE_LOW].min())
    entry.append(period.iloc[0, :][SourceDataColumns.QUOTE_CLOSE])
    return pd.Series(entry, index=[SourceDataColumns.QUOTE_OPEN, SourceDataColumns.QUOTE_HIGH, SourceDataColumns.QUOTE_LOW, SourceDataColumns.QUOTE_CLOSE])