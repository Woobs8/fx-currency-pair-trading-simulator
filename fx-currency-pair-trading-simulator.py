import argparse
import pandas as pd
from preprocessing.preprocessor import Preprocessor
from datautils.data_columns import PreprocessingColumns


def preprocessing(currency_pair: str, avg_func: str, short_window: int, long_window: int, price: str, no_cache: bool) -> pd.DataFrame:
    preprocessor = Preprocessor(args.currency_pair)
    preprocessor.initialize(no_cache)
    short_ma = preprocessor.get_moving_average(avg_func, short_window, price)
    short_ma.columns = [PreprocessingColumns.TIME, PreprocessingColumns.SHORT_AVG]
    long_ma = preprocessor.get_moving_average(avg_func, long_window, price)
    long_ma.columns = [PreprocessingColumns.TIME, PreprocessingColumns.LONG_AVG]
    return pd.merge(short_ma, long_ma, on=PreprocessingColumns.TIME, how='inner')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trading simulator for FX currency-pairs')
    parser.add_argument('currency_pair', type=str, help='name of FX currency-pair', choices=['eurusd'])
    parser.add_argument('--short', '--s', type=int, help='short window for moving average', required=True)
    parser.add_argument('--long', '--l', type=int, help='long window for moving average', required=True)
    parser.add_argument('--avg', type=str, help='moving average function', choices=['sma', 'ema'], default='ema')
    parser.add_argument('--price', '--p', type=str, help='the price to use for the selected tick resolution', choices=['open', 'close', 'high', 'low'], default='close')
    parser.add_argument('--tick', type=int, help='tick period (in minutes)', choices=[1, 60], default=1)
    parser.add_argument('--no-cache', '--nc', action='store_true', help='ignore caches and load data from source')

    args = parser.parse_args()
    moving_averages = preprocessing(args.currency_pair, args.avg, args.short, args.long, args.price, args.no_cache)
    print(moving_averages)