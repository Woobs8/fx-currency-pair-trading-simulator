from os import path, listdir
from datetime import datetime
from time import timezone
import pytz

CACHE_DIRECTORY = '.cache'
DATA_DIRECTORY = 'data'
OUTPUT_DIRECTORY = 'out'


def get_latest_source_modification(currency_pair: str, years: list = None) -> datetime:
    data_sources = get_data_sources(currency_pair, years)
    modification_times = map(get_modification_time, data_sources)
    return max(modification_times)


def get_data_sources(currency_pair: str, years: list = None) -> list:
    data_source_dir = '{}/{}'.format(get_data_dir(), currency_pair)
    dir_content = listdir(data_source_dir)
    if years:
        dir_content = filter_by_years(dir_content)
    only_zip_files = filter_zip_files(dir_content)
    return list(map(lambda file_name: '{}/{}'.format(data_source_dir, file_name), only_zip_files))


def get_data_dir() -> str:
    return get_abs_path_to_top_level_dir(DATA_DIRECTORY)


def get_abs_path_to_top_level_dir(dir: str):
    dir_name = path.dirname(__file__)
    data_path = path.join(dir_name, '../{}'.format(dir))
    return path.abspath(data_path)


def get_cache_dir() -> str:
    return get_abs_path_to_top_level_dir(CACHE_DIRECTORY)


def get_output_dir(simulation_id: str = None) -> str:
    output_dir = get_abs_path_to_top_level_dir(OUTPUT_DIRECTORY)
    if simulation_id is not None:
        return '{}/{}'.format(output_dir, simulation_id)
    else:
        return output_dir


def filter_by_years(files: list, years: list) -> list:
    return filter(lambda fp: extract_year_from_filename(fp) in years, files)


def extract_year_from_filename(file_name: str) -> int:
    return int(file_name.split('.')[0])


def filter_zip_files(files: list) -> list:
    return filter(lambda fp: fp.endswith('.zip'), files)


def get_modification_time(fp: str) -> datetime:
    modifification_ts = path.getmtime(fp)
    return datetime.utcfromtimestamp(modifification_ts)