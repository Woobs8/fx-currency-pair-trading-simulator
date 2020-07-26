import argparse
import pandas as pd
from caching.cache import Cache
from data_loading.fileutils import get_latest_source_modification
from data_loading.source_reader.hist_data_reader import HistDataReader
from data_loading.data_loader import DataLoader
from preprocessing.preprocessor import Preprocessor
from preprocessing.signal_strategy.signal_strategy_factory import SignalStrategyFactory
from preprocessing.stopping_strategy.stopping_strategy_factory import StoppingStrategyFactory
from analysis.summary import print_data_summary
from analysis.signal_analyzer import SignalAnalyzer


def initialize(currency_pair: str) -> None:
    cache = Cache(currency_pair)
    source_mod_time = get_latest_source_modification(currency_pair)
    if cache.cache_exists() and cache.get_data_mod_time() < source_mod_time:
        print('Cache invalid. Clearing cache.')
        cache.delete()


def data_loading(currency_pair: str, no_cache: bool) -> pd.DataFrame:
    source_reader = HistDataReader()
    loader = DataLoader(source_reader)
    if no_cache:
        print('Cache disabled.')
        data = loader.load_from_sources(currency_pair)
    else:
        data = loader.load(currency_pair)
    
    if data is not None:
        print_data_summary(data)
        return data
    else:
        raise RuntimeError('Unable to load data')


def preprocessing(currency_pair: str, data: pd.DataFrame, signal_strat: str, ma_fnc: str, short_window: int, long_window: int, quote: str, hyst: int, stop_strat: str, stop_profit: int, stop_loss: int, lookback: int, no_cache: bool) -> pd.DataFrame:
    signal_strategy = SignalStrategyFactory.get(signal_strat, avg_fnc=ma_fnc, short_window=short_window, long_window=long_window, quote=quote, hysteresis=hyst)
    stop_strategy = StoppingStrategyFactory.get(stop_strat, stop_profit=stop_profit, stop_loss=stop_loss, quote=quote)
    preprocessor = Preprocessor(currency_pair, signal_strategy, stop_strategy)
    if no_cache:
        return preprocessor.find_signals(data)
    else:
        return preprocessor.get_signals(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trading simulator for FX currency-pairs')
    parser.add_argument('currency_pair', type=str, help='name of FX currency-pair', choices=['eurusd'])
    parser.add_argument('--signal', type=str, help='strategy for detecting buy/sell signals', choices=['ma'], required=True)
    parser.add_argument('--mafnc', type=str, help='moving average function', choices=['sma', 'ema'])
    parser.add_argument('--short', type=int, help='short window for moving average (in minutes)')
    parser.add_argument('--long', type=int, help='long window for moving average (in minutes)')
    parser.add_argument('--quote', type=str, help='the quote to use for the selected tick resolution', choices=['open', 'close', 'high', 'low'], default='close')
    parser.add_argument('--tick', type=int, help='tick period (in minutes)', choices=[1, 60], default=1)
    parser.add_argument('--hyst', type=int, help='hysteresis (in pips)')
    parser.add_argument('--stop', type=str, help='strategy for stopping criterias', choices=['offset', 'fib'], required=True)
    parser.add_argument('--profit', type=int, help='delta pips for setting stop profit')
    parser.add_argument('--loss', type=int, help='delta pips for setting stop loss')
    parser.add_argument('--lookback', '--lb', type=int, help='duration (in minutes) to lookback when using fibonacci method for stopping criteria')
    parser.add_argument('--no-cache', '--nc', action='store_true', help='ignore caches and load data from source')

    args = parser.parse_args()
    data = data_loading(args.currency_pair, args.no_cache)
    signals = preprocessing(args.currency_pair, data, args.signal, args.mafnc, args.short, args.long, args.quote, args.hyst, args.stop, args.profit, args.loss, args.lookback, args.no_cache)
    print(signals)
    analyzer = SignalAnalyzer(data, signals)
    stats = analyzer.get_buy_stats(2019)
    print(stats)
