import pandas as pd
from datautils.cache import cache_valid, load_cache, create_cache
from datautils.source_loading import load_data_sources, get_latest_source_modification
from datautils.data_summary import print_data_summary

def load_data(currency_pair: str, no_cache:bool) -> pd.DataFrame:
    source_mod_time = get_latest_source_modification(currency_pair)
    cache_is_valid = cache_valid(currency_pair, source_mod_time)
    
    if (not no_cache) and cache_is_valid:
        print('Cache detected and validated. Loading data from cache.')
        data = load_cache(currency_pair)
    else:
        print('Cache disabled or not found. Loading data from sources.')
        data = load_data_sources(currency_pair)
    
    if data is not None and not data.empty:
        print('Successufully loaded data')
        print_data_summary(data)
    else:
        raise RuntimeError('Unable to load data')

    if not no_cache and (not cache_is_valid):
        print('Creating cache to speed up future invocations')
        create_cache(currency_pair, data, source_mod_time)
    return data