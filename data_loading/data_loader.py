import pandas as pd
from caching import Cache
from .source_reader.source_reader import SourceReader
from .resampling import resample_source
from utils.fileutils import get_latest_source_modification, get_data_sources
from shared import SourceDataColumns
import os

class DataLoader:

    DATA_DIRECTORY = 'data'

    def __init__(self, source_reader: SourceReader, tick_rate: str):
        self.source_reader = source_reader
        self.tick_rate = tick_rate


    def load(self, currency_pair: str) -> pd.DataFrame:
        cache = Cache.get()
        if cache.cache_exists() and cache.contains(self.tick_rate):
            print('Cache detected. Loading data from cache.')
            resampled_data = cache.fetch(self.tick_rate)
            if self.source_reader.TICK_RATE != self.tick_rate:
                data = cache.fetch(self.source_reader.TICK_RATE)
            else:
                data = resampled_data
        else:
            print('No cache found. Loading data from sources.')
            data, resampled_data = self.load_from_sources(currency_pair)

            print('Caching data to speed up future invocations.')
            if resampled_data is not data:
                cache.put(resampled_data, self.tick_rate)
            cache.put(data, self.source_reader.TICK_RATE)
            data_mod_time = get_latest_source_modification(currency_pair)
            cache.set_data_mod_time(data_mod_time)
        return data, resampled_data


    def load_from_sources(self, currency_pair: str, years: list = None) -> pd.DataFrame:
        print('Loading data from sources.')
        data_sources = get_data_sources(currency_pair, years)
        loaded_sources = list(map(self.load_data_source, data_sources))
        data = pd.concat(loaded_sources, axis=0).sort_index()
        if self.source_reader.TICK_RATE != self.tick_rate:
            print('Resampling data from tick rate [{}] to [{}]'.format(self.source_reader.TICK_RATE, self.tick_rate))
            resampled_data = resample_source(data, self.tick_rate)
        else:
            resampled_data = data
        return data, resampled_data


    def load_data_source(self, fp: str) -> pd.DataFrame:
        return self.source_reader.load_dataframe(fp)