from abc import ABC, abstractmethod
import pandas as pd


class SignalStrategy(ABC):

    @abstractmethod
    def find_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass