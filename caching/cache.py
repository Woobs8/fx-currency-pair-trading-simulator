from os import path, makedirs, remove
import pandas as pd
from .hdf5_storage import HDF5Storage
from datetime import datetime
from utils.fileutils import get_cache_dir


CACHE_DIRECTORY = '.cache'
META_KEY = 'meta'
LATEST_MOD_COL = 'latest_mod'


class Cache:

    currency_pair = None
    instance = None

    @classmethod
    def configure(cls, currency_pair: str) -> None:
        cls.currency_pair = currency_pair
    

    @classmethod
    def get(cls):
        if cls.currency_pair is None:
            raise RuntimeError('Cache not configured with currency_pair')
        if cls.instance is None:
            cls.instance = Cache(cls.currency_pair)
        return cls.instance


    def __init__(self, currency_pair: str):
        self.currency_pair = currency_pair
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
        self.storage.store(self.cache_path, df, key)

    
    def fetch(self, key: str, columns: list = None) -> pd.DataFrame:
        if not self.cache_exists():
            raise FileNotFoundError('No cache found for [{}]'.format(self.currency_pair))
        elif not self.contains(key):
            raise KeyError('No key [{}] found in cache [{}]'.format(key, self.currency_pair))
        return self.storage.load(self.cache_path, key)


    def contains(self, key: str, column: str = None) -> bool:
        return self.storage.contains(self.cache_path, key, column)

    
    def delete(self):
        if not self.cache_exists():
            raise FileNotFoundError('No cache found for [{}]'.format(self.currency_pair))
        return remove(self.cache_path)

    
    def set_data_mod_time(self, mod_time: datetime) -> None:
        mod_time_df = pd.DataFrame({LATEST_MOD_COL: mod_time}, index=[0])
        self.put(mod_time_df, META_KEY)

    
    def get_data_mod_time(self) -> datetime:
        mod_time_df = self.fetch(META_KEY)
        return pd.to_datetime(mod_time_df[LATEST_MOD_COL].dt.to_pydatetime())
