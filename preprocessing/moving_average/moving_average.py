from abc import ABC, abstractmethod
import pandas as pd


class MovingAverage(ABC):

    def __init__(self, window: int):
        self.window = window
        super().__init__()


    @abstractmethod
    def calc(self, data: pd.Series) -> pd.Series:
        pass