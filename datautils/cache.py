from os import path, makedirs
import pandas as pd
from datautils.hdf5_storage import HDF5Storage
from datetime import datetime

CACHE_DIRECTORY = '.cache'
CACHE_KEY = 'cache'
META_KEY = 'meta'
MOD_TIME_COLUMN = 'mod_time'


def cache_exists(currency_pair: str) -> bool:
    return path.exists(get_abs_cache_path(currency_pair))


def get_abs_cache_path(currency_pair: str):
    dir_name = path.dirname(__file__)
    cache_dir = path.join(dir_name, '../{}'.format(CACHE_DIRECTORY))
    cache_path = '{}/{}.h5'.format(cache_dir, currency_pair)
    return path.abspath(cache_path)


def cache_valid(currency_pair: str, mod_time: datetime) -> bool:
    if not cache_exists(currency_pair):
        return False
    
    cache_path = get_abs_cache_path(currency_pair)
    storage = HDF5Storage()
    meta_df = storage.load(cache_path, META_KEY)
    return mod_time <= pd.to_datetime(meta_df[MOD_TIME_COLUMN].dt.to_pydatetime())
    

def create_cache(currency_pair: str, df: pd.DataFrame, mod_time: datetime = None) -> None:
    cache_path = get_abs_cache_path(currency_pair)
    makedirs(path.dirname(cache_path), exist_ok=True)
    storage = HDF5Storage()
    storage.store(cache_path, df, CACHE_KEY)

    if mod_time is not None:
        meta_df = create_meta_df(mod_time)
        storage.store(cache_path, meta_df, META_KEY)


def create_meta_df(mod_time: datetime) -> pd.DataFrame:
    return pd.DataFrame({MOD_TIME_COLUMN: mod_time}, index=[0])


def load_cache(currency_pair: str) -> pd.DataFrame:
    cache_path = get_abs_cache_path(currency_pair)
    storage = HDF5Storage()
    return storage.load(cache_path, CACHE_KEY)