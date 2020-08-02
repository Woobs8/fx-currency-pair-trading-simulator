from .stopping_strategy import StoppingStrategy
from shared import SourceDataColumns, SignalColumns
import pandas as pd


class OffsetStoppingStrategy(StoppingStrategy):

    PIPS_SCALING = 1/100000

    def __init__(self, stop_profit: int, stop_loss: int, quote: str):
        self.stop_profit = stop_profit
        self.stop_profit_delta_pips = self.stop_profit * self.PIPS_SCALING
        self.stop_loss = stop_loss
        self.stop_loss_detlta_pips = self.stop_loss * self.PIPS_SCALING
        self.quote = quote
        super().__init__()


    def find_stopping_criteria(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        quotes = pd.merge(data, signals, left_index=True, right_index=True)
        buy_indices = (quotes[SignalColumns.BUY] == True).values
        sell_indices = (quotes[SignalColumns.SELL] == True).values
        stop_profit_criteria = self.calc_stop_profit(quotes[self.quote], buy_indices, sell_indices, self.stop_profit_delta_pips)
        stop_loss_criteria = self.calc_stop_loss(quotes[self.quote], buy_indices, sell_indices, self.stop_loss_detlta_pips)
        stopping_criteria = pd.merge(stop_profit_criteria, stop_loss_criteria, left_index=True, right_index=True)
        return stopping_criteria
    

    def calc_stop_profit(self, quote_series: pd.Series, buy_idcs: pd.Series, sell_idcs: pd.Series, delta: int) -> pd.Series:
        stop_profit = quote_series + delta*buy_idcs - delta*sell_idcs
        return stop_profit.rename(SignalColumns.STOP_PROFIT)


    def calc_stop_loss(self, quote_series: pd.Series, buy_idcs: pd.Series, sell_idcs: pd.Series, delta: int) -> pd.Series:
        stop_loss = quote_series - delta*buy_idcs + delta*sell_idcs
        return stop_loss.rename(SignalColumns.STOP_LOSS)


    def __repr__(self):
        return "offset_{}_{}_{}".format(self.stop_profit, self.stop_loss, self.quote)


    def __str__(self):
        return "offset_{}_{}_{}".format(self.stop_profit, self.stop_loss, self.quote)