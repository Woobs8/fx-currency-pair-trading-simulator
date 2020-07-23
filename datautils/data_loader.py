import pandas as pd
from datautils.cache import Cache
from datautils.source_loading import load_data_sources, get_latest_source_modification
from datautils.data_summary import print_data_summary
from datetime import datetime


class DataLoader:

    DATA_KEY = 'data'
    META_KEY = 'meta'
    LATEST_MOD_COL = 'latest_mod'

    def __init__(self, currency_pair: str):
        self.currency_pair = currency_pair
        self.source_mod_time = get_latest_source_modification(currency_pair)
        self.cache = Cache(self.currency_pair)


    def load(self, no_cache: bool = False) -> pd.DataFrame:
        if no_cache:
            print('Cache disabled. Loading data from sources.')
            data = load_data_sources(self.currency_pair)
        else:
            if self.validate_cache():
                print('Valid cache detected. Loading from cache.')
                data = self.cache.fetch(self.DATA_KEY)
            else:
                print('Cache invalid or not found. Loading data from sources.')
                data = load_data_sources(self.currency_pair)
                print('Creating cache to speed up future invocations')
                self.cache.put(data, self.DATA_KEY)
                self.update_cache_metadata()
        
        if data is not None and not data.empty:
            print('Successufully loaded data')
            print_data_summary(data)
        else:
            raise RuntimeError('Unable to load data')
        return data


    def validate_cache(self) -> bool:
        if not self.cache.cache_exists():
            return False
        meta_df = self.cache.fetch(self.META_KEY)
        cache_mod_time = pd.to_datetime(meta_df[self.LATEST_MOD_COL].dt.to_pydatetime())
        return self.source_mod_time <= cache_mod_time


    def update_cache_metadata(self) -> None:
        source_mod_time_df = pd.DataFrame({self.LATEST_MOD_COL: self.source_mod_time}, index=[0])
        self.cache.put(source_mod_time_df, self.META_KEY)