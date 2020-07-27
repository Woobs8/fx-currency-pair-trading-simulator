import pandas as pd
from caching.cache import Cache
from data_loading.source_reader.source_reader import SourceReader
from utils.fileutils import get_latest_source_modification, get_data_sources
from shared.columns import SourceDataColumns
import os

class DataLoader:

    DATA_DIRECTORY = 'data'
    DATA_CACHE_KEY = 'data'

    def __init__(self, source_reader: SourceReader):
        self.source_reader = source_reader


    def load(self, currency_pair: str) -> pd.DataFrame:
        cache = Cache.get()
        if cache.cache_exists():
            print('Cache detected. Loading data from cache.')
            data = cache.fetch(self.DATA_CACHE_KEY)
        else:
            print('No cache found. Loading data from sources.')
            data = self.load_from_sources(currency_pair)
            print('Caching data to speed up future invocations.')
            cache.put(data, self.DATA_CACHE_KEY)
            data_mod_time = get_latest_source_modification(currency_pair)
            cache.set_data_mod_time(data_mod_time)
        return data


    def load_from_sources(self, currency_pair: str, years: list = None) -> pd.DataFrame:
        print('Loading data from sources.')
        data_sources = get_data_sources(currency_pair, years)
        loaded_sources = list(map(self.load_data_source, data_sources))
        return pd.concat(loaded_sources, axis=0).sort_index()


    def load_data_source(self, fp: str) -> pd.DataFrame:
        return self.source_reader.load_dataframe(fp)