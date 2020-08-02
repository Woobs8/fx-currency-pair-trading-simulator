import pandas as pd
from caching import Cache
from utils.fileutils import get_latest_source_modification
from data_loading import DataLoader, HistDataReader
from preprocessing import SignalStrategyFactory, StoppingStrategyFactory, Preprocessor
from analysis import print_data_summary
from argparse import Namespace


def init(args) -> (pd.DataFrame, pd.DataFrame):
    initialize_cache(args.currency_pair, args.tick_rate)
    data = load_data(args.currency_pair, args.tick_rate, args.no_cache)
    signals = preprocess_signals(data, args)
    return data, signals


def initialize_cache(currency_pair: str, tick_rate: str) -> None:
    Cache.configure(currency_pair, tick_rate)
    cache = Cache.get()
    source_mod_time = get_latest_source_modification(currency_pair)
    if cache.cache_exists() and cache.get_data_mod_time() < source_mod_time:
        print('Cache invalid. Clearing cache.')
        cache.delete()


def load_data(currency_pair: str, tick_rate: str, no_cache: bool) -> pd.DataFrame:
    source_reader = HistDataReader()
    loader = DataLoader(source_reader, tick_rate)
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
    

def preprocess_signals(data: pd.DataFrame, args: Namespace) -> pd.DataFrame:
    signal_strategy = SignalStrategyFactory.get('ma', **signal_strat_argument_parser(args))
    stopping_strat_argument_parser(args)
    stop_strategy = StoppingStrategyFactory.get(args.stopping_strat, **stopping_strat_argument_parser(args))
    preprocessor = Preprocessor(signal_strategy, stop_strategy)
    if args.no_cache:
        return preprocessor.find_signals(data)
    else:
        return preprocessor.get_signals(data)


def signal_strat_argument_parser(args: Namespace) -> dict:
    arguments = {}
    for k, v in args.__dict__.items():
        if k in ['ma_fnc', 'short_window', 'long_window', 'quote', 'delta', 'confidence_window'] and v is not None:
            arguments[k] = v
    return arguments


def stopping_strat_argument_parser(args: Namespace) -> dict:
    arguments = {}
    for k, v in args.__dict__.items():
        if k in ['stop_profit', 'stop_loss', 'quote', 'retracement'] and v is not None:
            arguments[k] = v
    return arguments