from caching.cache import Cache
import pandas as pd
from preprocessing.moving_average import ema, sma
from preprocessing.signal_identification import find_signals
from data_loading.source_loading import get_latest_source_modification, load_data_sources
from data_loading.summary import print_data_summary
from shared.columns import SourceDataColumns, PreprocessingColumns, MetadataColumns


class Preprocessor:

    META_CACHE_KEY = 'meta'
    DATA_CACHE_KEY = 'data'

    def __init__(self, currency_pair: str):
        self.currency_pair = currency_pair
        self.cache = Cache(self.currency_pair)
        self.source_mod_time = get_latest_source_modification(currency_pair)


    def initialize(self, no_cache: bool = False):
        self.no_cache = no_cache
        if self.cache.cache_exists() and not self.validate_cache():
            print('Cache invalid. Clearing cache.')
            self.cache.delete()
        self.data = self.load_data()


    def validate_cache(self) -> bool:
        meta_df = self.get_cache_metadata()
        cache_mod_time = pd.to_datetime(meta_df[MetadataColumns.LATEST_MODIFICATION].dt.to_pydatetime())
        return self.source_mod_time <= cache_mod_time


    def get_cache_metadata(self) -> pd.DataFrame:
            return self.cache.fetch(self.META_CACHE_KEY)


    def load_data(self) -> pd.DataFrame:
        if self.no_cache:
            print('Cache disabled. Loading data from sources.')
            data = load_data_sources(self.currency_pair)
        else:
            if self.cache.cache_exists():
                print('Cache detected. Loading data from cache.')
                data = self.cache.fetch(self.DATA_CACHE_KEY)
            else:
                print('No cache found. Loading data from sources.')
                data = load_data_sources(self.currency_pair)
                print('Caching data to speed up future invocations.')
                self.cache.put(data, self.DATA_CACHE_KEY)
                self.update_cache_metadata()
        
        if data is not None:
            print_data_summary(data)
            return data
        else:
            raise RuntimeError('Unable to load data')


    def update_cache_metadata(self) -> None:
        source_mod_time_df = pd.DataFrame({MetadataColumns.LATEST_MODIFICATION: self.source_mod_time}, index=[0])
        self.cache.put(source_mod_time_df, self.META_CACHE_KEY)
            

    def get_signals(self, avg_func: str, short_window: int, long_window: int, price: str, hysteresis: int) -> pd.DataFrame:
        cache_key = '{}_{}_{}_{}_{}'.format(avg_func, short_window, long_window, price, hysteresis)
        if not self.no_cache:
            cached_signals = self.fetch_from_preprocessing_cache(cache_key)

        if self.no_cache or cached_signals.empty:
            print('Finding signals for [fnc={}, sw={}, lw={}, price={}, hyst={}]'.format(avg_func, short_window, long_window, price, hysteresis))
            ma = self.get_moving_averages(avg_func, short_window, long_window, price)
            signals = find_signals(ma, hysteresis)
            if not self.no_cache:
                print('Caching result for [{}].'.format(cache_key))
                self.cache.put(signals, cache_key)
            return signals
        else:
            return cached_signals

    
    def get_moving_averages(self, fnc: str, short_window: int, long_window: int, price: str) -> pd.DataFrame:
        short_ma = self.get_moving_average(fnc, short_window, price)
        short_ma.columns = [PreprocessingColumns.TIME, PreprocessingColumns.SHORT_AVG]
        long_ma = self.get_moving_average(fnc, long_window, price)
        long_ma.columns = [PreprocessingColumns.TIME, PreprocessingColumns.LONG_AVG]
        return pd.merge(short_ma, long_ma, on=PreprocessingColumns.TIME, how='inner')

    
    def get_moving_average(self, avg_func: str, window: int, price: str) -> pd.DataFrame:
        cache_key = '{}{}_{}'.format(avg_func, window, price)
        if not self.no_cache:
            cached_ma = self.fetch_from_preprocessing_cache(cache_key)

        if self.no_cache or cached_ma.empty:
            print('Calculating moving average for [fnc={}, w={}, price={}]'.format(avg_func, window, price))
            ma = self.calc_moving_average(avg_func, window, price)

            if not self.no_cache:
                print('Caching result for [{}].'.format(cache_key))
                self.cache.put(ma, cache_key)
            return ma
        else:
            return cached_ma


    def fetch_from_preprocessing_cache(self, key: str) -> pd.DataFrame:
        if self.cache.cache_exists() and self.cache.contains(key):
            print('Fetching result for [{}] from cache'.format(key))
            return self.cache.fetch(key)
        else:
            return pd.DataFrame()


    def calc_moving_average(self, fnc: str, window: int, price: str) -> pd.DataFrame:
        if fnc is 'ema':
            ma = ema(self.data[price], window)
        else:
            ma = sma(self.data[price], window)

        ma_time = self.data[SourceDataColumns.TIME]
        combined_df = pd.concat([ma_time, ma], axis=1)
        combined_df.columns = [PreprocessingColumns.TIME, PreprocessingColumns.MOVING_AVERAGE]
        return combined_df