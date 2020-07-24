import pandas as pd

class HDF5Storage:

    def store(self, fp: str, df: pd.DataFrame, name: str) -> None:
        with pd.HDFStore(fp) as hdf:
            hdf.put(name, df, format='table', data_columns=True)  
    

    def load(self, fp: str, name: str, columns: list = None) -> pd.DataFrame:
        return pd.read_hdf(fp, name, columns=columns)

    
    def contains(self, fp: str, name: str, column: str = None) -> bool:
        with pd.HDFStore(fp) as hdf:
            if column is not None:
                return column in hdf.get_node('{}/table'.format(name)).description._v_names
            else:
                return '/{}'.format(name) in hdf.keys()