from os import path, makedirs, remove
import pandas as pd
from .hdf5_storage import HDF5Storage
from datetime import datetime
from utils.fileutils import get_cache_dir


class Cache:

    META_KEY = 'meta'
    LATEST_MOD_COL = 'latest_mod'

    currency_pair = None
    group = None
    instance = None

    @classmethod
    def configure(cls, currency_pair: str, group: str = None):
        cls.currency_pair = currency_pair
        cls.group = group
        cls.instance = Cache(cls.currency_pair, cls.group)
        return cls.instance
    

    @classmethod
    def get(cls):
        if cls.currency_pair is None:
            raise RuntimeError('Cache not configured with currency_pair')

        if cls.instance is None:
            cls.instance = Cache(cls.currency_pair, cls.group)
        return cls.instance


    @classmethod
    def __enter__(cls):
        return cls


    @classmethod
    def __exit__(cls, typ, value, tb):
        cls.currency_pair = None
        cls.group = None
        cls.instance = None


    def __init__(self, currency_pair: str, group: str = None):
        self.currency_pair = currency_pair
        self.group = group
        self.cache_path = self.get_abs_cache_path(currency_pair)
        self.storage = HDF5Storage()


    def get_abs_cache_path(self, currency_pair: str):
        dir_name = path.dirname(__file__)
        cache_dir = get_cache_dir()
        cache_path = '{}/{}.h5'.format(cache_dir, currency_pair)
        return path.abspath(cache_path)


    def cache_exists(self) -> bool:
        return path.exists(self.cache_path)
        
    
    def put(self, df: pd.DataFrame, key: str) -> None:
        if not self.cache_exists():
            makedirs(path.dirname(self.cache_path), exist_ok=True)
        self.storage.store(self.cache_path, df, key, group=self.group)

    
    def fetch(self, key: str) -> pd.DataFrame:
        if not self.cache_exists():
            raise FileNotFoundError('No cache found for [{}, ticks={}]'.format(self.currency_pair, self.group))
        elif not self.contains(key):
            raise KeyError('No key [{}] found in cache [{}, ticks={}]'.format(key, self.currency_pair, self.group))
        return self.storage.load(self.cache_path, key, group=self.group)


    def contains(self, key: str) -> bool:
        return self.storage.contains(self.cache_path, key, group=self.group)


    def clear_all_keys(self):
        if not self.cache_exists():
            raise FileNotFoundError('No cache found for [{}, ticks={}]'.format(self.currency_pair, self.group))
        self.storage.clear(self.cache_path)

    
    def clear(self):
        if not self.cache_exists():
            raise FileNotFoundError('No cache found for [{}, ticks={}]'.format(self.currency_pair, self.group))
        return self.storage.delete(self.cache_path, self.group)

    
    def set_data_mod_time(self, mod_time: datetime) -> None:
        mod_time_df = pd.DataFrame({self.LATEST_MOD_COL: mod_time}, index=[0])
        self.put(mod_time_df, self.META_KEY)

    
    def get_data_mod_time(self) -> datetime:
        mod_time_df = self.fetch(self.META_KEY)
        return pd.to_datetime(mod_time_df[self.LATEST_MOD_COL].dt.to_pydatetime())

