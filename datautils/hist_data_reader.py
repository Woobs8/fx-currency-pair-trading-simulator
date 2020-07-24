import pandas as pd
from zipfile import ZipFile
import os
from time import timezone
from datautils.csv_reader import CsvReader
from datautils.data_columns import SourceDataColumns


class HistDataReader:
    def __init__(self, fp: str):            
        self.fp = fp
        self.sep = ';'
        self.header = None
        self.columns = [0, 1, 2, 3, 4]
        self.column_names = [SourceDataColumns.TIME, 
                            SourceDataColumns.PRICE_OPEN, 
                            SourceDataColumns.PRICE_HIGH, 
                            SourceDataColumns.PRICE_LOW, 
                            SourceDataColumns.PRICE_CLOSE]
        self.date_column = 0
        self.data_tz = 'US/Eastern'
        self.local_tz = -timezone # tz is returned as seconds west of UTC (meaning the sign is reversed compared to usual notation)
        self.csv_reader = CsvReader(self.sep, self.columns, self.column_names, self.header, self.date_column, self.data_tz, self.local_tz)

        if fp.endswith('.zip'):
            self.load_fnc = self.load_zipped_csv
        elif fp.endswith('.csv'):
            self.load_fnc = self.csv_reader.load
        else:
            raise ValueError('Invalid file type {}. Only .csv and .zip supported'.format(fp))

    def load_dataframe(self) -> pd.DataFrame:
        return self.load_fnc(self.fp)

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