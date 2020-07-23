import pandas as pd

class CsvReader:
    def __init__(self, 
                sep: str = ';', 
                columns: list = None, 
                column_names: list = None, 
                header: list = None, 
                date_column: int = None,
                data_tz = None,
                local_tz = None):
        self.sep = sep
        self.columns = columns
        self.column_names = column_names
        self.header = header
        self.date_column = date_column
        self.data_tz = data_tz
        self.local_tz = local_tz


    def load(self, fp: str) -> pd.DataFrame:
        df =  pd.read_csv(fp, sep=self.sep, usecols=self.columns, names=self.column_names, header=self.header, parse_dates=[self.date_column])
        if self.data_tz is not None:
            df.iloc[:, self.date_column] = self.set_timezone(df.iloc[:, self.date_column])

        if self.local_tz is not None:
            df.iloc[:, self.date_column] = self.convert_timezone(df.iloc[:, self.date_column])
        return df


    def set_timezone(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dt.tz_localize(self.data_tz)


    def convert_timezone(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dt.tz_convert(self.local_tz)