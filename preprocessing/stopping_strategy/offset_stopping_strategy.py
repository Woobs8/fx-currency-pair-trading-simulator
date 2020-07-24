from preprocessing.stopping_strategy.stopping_strategy import StoppingStrategy
from shared.columns import SourceDataColumns, PreprocessingColumns
import pandas as pd


class OffsetStoppingStrategy(StoppingStrategy):


    PIPS_SCALING = 1/10000


    def find_stopping_criteria(self, signals: pd.DataFrame, data: pd.DataFrame, price: str) -> pd.DataFrame:
        prices = pd.merge(data, signals, how='inner', left_on=[SourceDataColumns.TIME], right_on=[PreprocessingColumns.TIME])
        buy_indices = prices[PreprocessingColumns.BUY] == True
        sell_indices = prices[PreprocessingColumns.SELL] == True
        stop_profit_criteria = self.calc_stop_profit(prices, buy_indices, sell_indices, price, self.stop_profit)
        stop_loss_criteria = self.calc_stop_loss(prices, buy_indices, sell_indices, price, self.stop_loss)
        stopping_criteria = pd.concat([prices[PreprocessingColumns.TIME], stop_profit_criteria, stop_loss_criteria], axis=1)
        stopping_criteria.columns = [PreprocessingColumns.TIME, PreprocessingColumns.STOP_PROFIT, PreprocessingColumns.STOP_LOSS]
        return stopping_criteria
    

    def calc_stop_profit(self, prices: pd.DataFrame, buy_idcs: pd.Series, sell_idcs: pd.Series, price: str, delta: int) -> pd.Series:
        stop_profit = prices[price] + delta*buy_idcs - delta*sell_idcs
        return stop_profit


    def calc_stop_loss(self, prices: pd.DataFrame, buy_idcs: pd.Series, sell_idcs: pd.Series, price: str, delta: int) -> pd.Series:
        stop_loss = prices[price] - delta*buy_idcs + delta*sell_idcs
        return stop_loss


    def __repr__(self):
        return "offset"


    def __str__(self):
        return "offset"