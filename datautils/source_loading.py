import os
import pandas as pd
from datautils.hist_data_reader import HistDataReader
from datautils.fileutils import get_modification_time
from datetime import datetime

DATA_DIRECTORY = 'data'

def load_data_sources(currency_pair: str, years: list = None) -> pd.DataFrame:
    data_sources = get_data_sources(currency_pair, years)
    loaded_sources = list(map(load_data_source, data_sources))
    df = pd.concat(loaded_sources, axis=0)
    return df.sort_values(by=['date'])


def get_data_sources(currency_pair: str, years: list = None) -> list:
    data_source_dir = '{}/{}'.format(get_data_dir(), currency_pair)
    dir_content = os.listdir(data_source_dir)
    if years:
        dir_content = filter_by_years(dir_content)
    only_zip_files = filter_zip_files(dir_content)
    return list(map(lambda file_name: '{}/{}'.format(data_source_dir, file_name), only_zip_files))


def get_data_dir() -> str:
    dir_name = os.path.dirname(__file__)
    data_path = os.path.join(dir_name, '../{}'.format(DATA_DIRECTORY))
    return os.path.abspath(data_path)


def filter_by_years(files: list, years: list) -> list:
    return filter(lambda fp: extract_year_from_filename(fp) in years, files)


def extract_year_from_filename(file_name: str) -> int:
    return int(file_name.split('.')[0])


def filter_zip_files(files: list) -> list:
    return filter(lambda fp: fp.endswith('.zip'), files)


def load_data_source(fp: str) -> pd.DataFrame:
    reader = HistDataReader(fp)
    return reader.load_dataframe()

def get_latest_source_modification(currency_pair: str, years: list = None) -> datetime:
    data_sources = get_data_sources(currency_pair, years)
    modification_times = map(get_modification_time, data_sources)
    return max(modification_times)