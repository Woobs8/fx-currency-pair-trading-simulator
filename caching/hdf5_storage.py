import pandas as pd

class HDF5Storage:

    def store(self, fp: str, df: pd.DataFrame, name: str, group: str = None) -> None:
        with pd.HDFStore(fp) as hdf:
            key = '{}/{}'.format(group if group is not None else '', name)
            hdf.put(key, df, format='table', data_columns=True)  
    

    def load(self, fp: str, name: str, group: str = None) -> pd.DataFrame:
        key = '{}/{}'.format(group if group is not None else '', name)
        return pd.read_hdf(fp, key)

    
    def contains(self, fp: str, name: str, group: str = None) -> bool:
        with pd.HDFStore(fp) as hdf:
            key = '/{}/{}'.format(group if group is not None else '', name)
            return key in hdf.keys()


    def delete(self, fp: str, group: str) -> None:
        with pd.HDFStore(fp) as hdf:
            hdf.remove(group)