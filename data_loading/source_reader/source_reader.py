from abc import ABC, abstractmethod
import pandas as pd


class SourceReader(ABC):

    @abstractmethod
    def load_dataframe(self, fp: str) -> pd.DataFrame:
        pass