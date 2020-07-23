import pandas as pd

class HDF5Storage:

    def store(self, fp: str, df: pd.DataFrame, name: str) -> None:
        with pd.HDFStore(fp) as hdf:
            hdf.put(name, df, format='table', data_columns=True)
    

    def load(self, fp: str, name: str) -> pd.DataFrame:
        return pd.read_hdf(fp, name)

    
    def contains(self, fp: str, name: str) -> bool:
        with pd.HDFStore(fp) as hdf:
            return '/{}'.format(name) in hdf.keys()