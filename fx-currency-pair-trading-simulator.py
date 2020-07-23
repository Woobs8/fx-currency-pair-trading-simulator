import argparse
from datautils.data_loading import load_data
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trading simulator for FX currency-pairs')
    parser.add_argument('currency_pair', metavar='currency-pair', type=str, help='name of FX currency-pair', choices=['eurusd'])
    parser.add_argument('--short', metavar='short avg', type=int, help='short window for moving average', required=True)
    parser.add_argument('--long', metavar='long avg', type=int, help='long window for moving average', required=True)
    parser.add_argument('--avg', metavar='avg fnc', type=str, help='moving average function', choices=['ema'], default='ema')
    parser.add_argument('--res', metavar='resolution', type=int, help='tick resolution (in minutes)', default=60)
    parser.add_argument('--no-cache', action='store_true', help='ignore caches and load data from source')

    args = parser.parse_args()
    data = load_data(args.currency_pair, args.no_cache)