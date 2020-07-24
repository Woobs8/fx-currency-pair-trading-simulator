import argparse
import pandas as pd
from preprocessing.preprocessor import Preprocessor
from preprocessing.stopping_strategy.stopping_strategy_builder import StoppingStrategyBuilder


def preprocessing(currency_pair: str, avg_func: str, short_window: int, long_window: int, price: str, hyst: int, stop_strat: str, stop_profit: int, stop_loss: int, lookback: int, no_cache: bool) -> pd.DataFrame:
    preprocessor = Preprocessor(args.currency_pair)
    preprocessor.initialize(no_cache)
    stop_strategy = StoppingStrategyBuilder.get_strategy(stop_strat, stop_profit, stop_loss, lookback)
    return preprocessor.get_signals(avg_func, short_window, long_window, price, hyst, stop_strategy)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trading simulator for FX currency-pairs')
    parser.add_argument('currency_pair', type=str, help='name of FX currency-pair', choices=['eurusd'])
    parser.add_argument('--avg', type=str, help='moving average function', choices=['sma', 'ema'], default='ema')
    parser.add_argument('--short', type=int, help='short window for moving average (in minutes)', required=True)
    parser.add_argument('--long', type=int, help='long window for moving average (in minutes)', required=True)
    parser.add_argument('--price', type=str, help='the price to use for the selected tick resolution', choices=['open', 'close', 'high', 'low'], default='close')
    parser.add_argument('--tick', type=int, help='tick period (in minutes)', choices=[1, 60], default=1)
    parser.add_argument('--hyst', type=int, help='hysteresis tolerance (in pips)', required=True)
    parser.add_argument('--stop', type=str, help='strategy for stopping criterias', choices=['offset', 'fib'], required=True)
    parser.add_argument('--profit', type=int, help='delta pips for setting stop profit')
    parser.add_argument('--loss', type=int, help='delta pips for setting stop loss')
    parser.add_argument('--lookback', '--lb', type=int, help='duration (in minutes) to lookback when using fibonacci method for stopping criteria')
    parser.add_argument('--no-cache', '--nc', action='store_true', help='ignore caches and load data from source')

    args = parser.parse_args()
    signals = preprocessing(args.currency_pair, args.avg, args.short, args.long, args.price, args.hyst, args.stop, args.profit, args.loss, args.lookback, args.no_cache)
    print(signals)