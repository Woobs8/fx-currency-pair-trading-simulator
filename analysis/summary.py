import pandas as pd
from math import floor
from datetime import datetime
from shared import SourceDataColumns

def print_data_summary(data: pd.DataFrame) -> None:
    entries, tick_rate, start, stop = summarize_data(data)
    print('Data summary:')
    print('\tStart: {}'.format(start))
    print('\tStop: {}'.format(stop))
    print('\tTicks: {}'.format(entries))
    print('\tTick rate : {} min.'.format(tick_rate))


def summarize_data(data: pd.DataFrame) -> (int, int, datetime, datetime):
    entries, cols = data.shape
    tick_rate = calc_tick_rate(data)
    start = get_start_time(data)
    stop = get_stop_time(data)
    return entries, tick_rate, start, stop
    

def calc_tick_rate(data: pd.DataFrame) -> int:
    delta = data.iloc[:2,:].index.to_series().diff().astype('timedelta64[m]').mean()
    return floor(delta)


def get_start_time(data: pd.DataFrame) -> datetime:
    return data.index[0].to_pydatetime()


def get_stop_time(data: pd.DataFrame) -> datetime:
    return data.index[-1].to_pydatetime()