import pandas as pd

class CsvReader:
    def __init__(self, 
                sep: str = ';', 
                columns: list = None, 
                column_names: list = None, 
                header: list = None, 
                time_column: int = None,
                data_tz = None,
                local_tz = None):
        self.sep = sep
        self.columns = columns
        self.column_names = column_names
        self.header = header
        self.time_column = time_column
        self.data_tz = data_tz
        self.local_tz = local_tz


    def load(self, fp: str) -> pd.DataFrame:
        df =  pd.read_csv(fp, sep=self.sep, usecols=self.columns, names=self.column_names, header=self.header, parse_dates=[self.time_column], index_col=self.time_column)
        if self.data_tz is not None:
            df = df.tz_localize(self.data_tz)

        if self.local_tz is not None:
           df = df.tz_convert(self.local_tz)
        return df


    def set_timezone(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.tz_localize(self.data_tz)


    def convert_timezone(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.tz_convert(self.local_tz)