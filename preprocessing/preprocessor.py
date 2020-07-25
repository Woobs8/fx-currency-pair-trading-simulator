from caching.cache import Cache
import pandas as pd
from preprocessing.signal_strategy.signal_strategy import SignalStrategy
from preprocessing.stopping_strategy.stopping_strategy import StoppingStrategy
from shared.columns import SourceDataColumns, PreprocessingColumns


class Preprocessor:

    def __init__(self, currency_pair: str, signal_strat: SignalStrategy, stop_strat: StoppingStrategy):
        self.currency_pair = currency_pair
        self.cache = Cache(self.currency_pair)
        self.signal_strat = signal_strat
        self.stop_strat = stop_strat
            

    def get_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        cache_key = '{}__{}__{}'.format(self.currency_pair, self.signal_strat, self.stop_strat)

        if self.cache.cache_exists and self.cache.contains(cache_key):
            print('Loading signals for [{}] from cache.'.format(cache_key))
            signals = self.cache.fetch(cache_key)
        else:
            signals = self.find_signals(data)
            print('Caching result for [{}].'.format(cache_key))
            self.cache.put(signals, cache_key)
        return signals


    def find_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        print('Finding signals for [signal_strat={}, stopping_strat={}].'.format(self.signal_strat, self.stop_strat))
        signals = self.signal_strat.find_signals(data)
        stopping_criterias = self.stop_strat.find_stopping_criteria(signals, data)
        return pd.merge(signals, stopping_criterias, how='inner', on=PreprocessingColumns.TIME)