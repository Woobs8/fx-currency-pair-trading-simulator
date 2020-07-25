from preprocessing.stopping_strategy.stopping_strategy import StoppingStrategy
from shared.columns import SourceDataColumns, PreprocessingColumns
import pandas as pd


class OffsetStoppingStrategy(StoppingStrategy):

    PIPS_SCALING = 1/10000

    def __init__(self, stop_profit: int, stop_loss: int, quote: str):
        self.stop_profit = stop_profit
        self.stop_loss = stop_loss
        self.quote = quote
        super().__init__()


    def find_stopping_criteria(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        quotes = pd.merge(data, signals, how='inner', left_on=[SourceDataColumns.TIME], right_on=[PreprocessingColumns.TIME])
        buy_indices = quotes[PreprocessingColumns.BUY] == True
        sell_indices = quotes[PreprocessingColumns.SELL] == True
        stop_profit_criteria = self.calc_stop_profit(quotes[self.quote], buy_indices, sell_indices, self.stop_profit)
        stop_loss_criteria = self.calc_stop_loss(quotes[self.quote], buy_indices, sell_indices, self.stop_loss)
        stopping_criteria = pd.concat([quotes[PreprocessingColumns.TIME], stop_profit_criteria, stop_loss_criteria], axis=1)
        stopping_criteria.columns = [PreprocessingColumns.TIME, PreprocessingColumns.STOP_PROFIT, PreprocessingColumns.STOP_LOSS]
        return stopping_criteria
    

    def calc_stop_profit(self, quotes: pd.DataFrame, buy_idcs: pd.Series, sell_idcs: pd.Series, delta: int) -> pd.Series:
        stop_profit = quotes + delta*buy_idcs - delta*sell_idcs
        return stop_profit


    def calc_stop_loss(self, quotes: pd.DataFrame, buy_idcs: pd.Series, sell_idcs: pd.Series, delta: int) -> pd.Series:
        stop_loss = quotes - delta*buy_idcs + delta*sell_idcs
        return stop_loss


    def __repr__(self):
        return "offset_{}_{}_{}".format(self.stop_profit, self.stop_loss, self.quote)


    def __str__(self):
        return "offset_{}_{}_{}".format(self.stop_profit, self.stop_loss, self.quote)