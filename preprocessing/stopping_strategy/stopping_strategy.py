from abc import ABC, abstractmethod
import pandas as pd


class StoppingStrategy(ABC):

    @abstractmethod
    def find_stopping_criteria(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        pass