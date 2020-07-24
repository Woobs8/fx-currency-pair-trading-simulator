from datautils.cache import Cache
import pandas as pd
from preprocessing.moving_average import ema, sma
from datautils.source_loading import get_latest_source_modification, load_data_sources
from datautils.data_summary import print_data_summary
from datautils.data_columns import SourceDataColumns, PreprocessingColumns, MetadataColumns


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
        print('Loading data...')
        if self.no_cache:
            print('Cache disabled. Loading data from sources.')
            data = load_data_sources(self.currency_pair)
        else:
            if self.cache.cache_exists():
                print('Cache detected. Loading from cache.')
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


    def get_moving_average(self, avg_func: str, window: int, price: str) -> pd.DataFrame:
        cache_key = '{}{}'.format(avg_func, window)
        cached_df = self.fetch_from_preprocessing_cache(cache_key)
        if not self.no_cache and not cached_df.empty:
            print('Fetching result for [{}] from cache'.format(cache_key))
            return cached_df
        else:
            ma = self.calc_moving_average(avg_func, window, price)
            ma_time = self.data[SourceDataColumns.TIME]
            combined_df = pd.concat([ma_time, ma], axis=1)
            combined_df.columns = [PreprocessingColumns.TIME, PreprocessingColumns.MOVING_AVERAGE]

            if not self.no_cache:
                print('Caching result for [{}].'.format(cache_key))
                self.cache.put(combined_df, cache_key)
            return combined_df


    def fetch_from_preprocessing_cache(self, key: str) -> pd.DataFrame:
        if self.cache.cache_exists() and self.cache.contains(key):
            return self.cache.fetch(key)
        else:
            return pd.DataFrame()


    def calc_moving_average(self, fnc: str, window: int, price: str) -> pd.Series:
        if fnc is 'ema':
            return ema(self.data[price], window)
        else:
            return sma(self.data[price], window)
            

