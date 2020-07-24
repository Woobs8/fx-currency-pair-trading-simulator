from abc import ABC, abstractmethod
import pandas as pd


class StoppingStrategy(ABC):

    def __init__(self, stop_profit: int = None, stop_loss: int = None, lookback: int = None):
        self.stop_profit = stop_profit
        self.stop_loss = stop_loss
        self.lookback = lookback
        super().__init__()


    @abstractmethod
    def find_stopping_criteria(self, signals: pd.DataFrame, data: pd.DataFrame, price: str) -> pd.DataFrame:
        pass

    
    def __repr__(self):
        return "abstract"


    def __str__(self):
        return "abstract"