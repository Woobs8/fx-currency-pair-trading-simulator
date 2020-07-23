import argparse
from datautils.data_loader import DataLoader
from preprocessing.moving_average import ema
import pandas as pd

def load_data(currency_pair: str, no_cache: bool) -> pd.DataFrame:
    loader = DataLoader(currency_pair)
    return loader.load(no_cache)
    

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
    loader = DataLoader(args.currency_pair)
    data = loader.load(args.no_cache)