import pandas as pd
from .source_reader import SourceReader
from ..csv_reader import CsvReader
from shared import SourceDataColumns
from zipfile import ZipFile
import os
from time import timezone


class HistDataReader(SourceReader):

    TICK_RATE = 'min'

    def __init__(self):
        self.sep = ';'
        self.header = None
        self.columns = [0, 1, 2, 3, 4]
        self.column_names = ['time',
                            SourceDataColumns.QUOTE_OPEN, 
                            SourceDataColumns.QUOTE_HIGH, 
                            SourceDataColumns.QUOTE_LOW, 
                            SourceDataColumns.QUOTE_CLOSE]
        self.time_column = 0
        self.data_tz = 'US/Eastern'
        self.local_tz = 'UTC'#-timezone # tz is returned as seconds west of UTC (meaning the sign is reversed compared to usual notation)
        self.csv_reader = CsvReader(self.sep, self.columns, self.column_names, self.header, self.time_column, self.data_tz, self.local_tz)


    def load_dataframe(self, fp: str) -> pd.DataFrame:
        if fp.endswith('.zip'):
            return self.load_zipped_csv(fp)
        elif fp.endswith('.csv'):
            return self.csv_reader.load(fp)
        else:
            raise ValueError('Invalid file type {}. Only .csv and .zip supported'.format(fp))  


    def load_zipped_csv(self, fp: str) -> pd.DataFrame:
        with ZipFile(fp) as zf:
            csv_fp = self.get_csv_files_in_archive(zf)[0]
            with zf.open(csv_fp) as csv:
                return self.csv_reader.load(csv)


    def get_csv_files_in_archive(self, zip_file: ZipFile) -> list:
        csv_files = [name for name in zip_file.namelist() if name.endswith('.csv')]
        if len(csv_files) > 0:
            return csv_files
        else:
            raise FileNotFoundError('No .csv files found in archive')