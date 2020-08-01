from .stopping_strategy import StoppingStrategy
from shared import SourceDataColumns, SignalColumns
import pandas as pd
from tqdm import tqdm
import numpy as np


class FibonacciStoppingStrategy(StoppingStrategy):

    PIPS_SCALING = 1/10000

    def __init__(self, retracement: float, stop_loss: int, quote: str):
        self.retracement = retracement
        self.stop_loss = stop_loss
        self.stop_loss_detlta_pips = self.stop_loss * self.PIPS_SCALING
        self.quote = quote
        super().__init__()


    def find_stopping_criteria(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        quotes = pd.merge(data, signals, left_index=True, right_index=True)
        buy_indices = (quotes[SignalColumns.BUY] == True).values
        sell_indices = (quotes[SignalColumns.SELL] == True).values
        stop_loss_criteria = self.calc_stop_loss(quotes[self.quote], buy_indices, sell_indices, self.stop_loss_detlta_pips)
        stop_profit_criteria = self.calc_stop_profit(quotes, data)
        stopping_criteria = pd.merge(stop_profit_criteria, stop_loss_criteria, left_index=True, right_index=True)
        return stopping_criteria


    def calc_stop_profit(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.Series:
        delta = [None] * signals.shape[0]
        progress = tqdm(range(2, len(delta)))
        progress.set_description('Calculating stopping criteria')
        for i in progress:
            signal = signals.iloc[i,:]
            prev_reverse_signal = signals.iloc[i-1, :]
            prev_same_signal = signals.iloc[i-2, :]
            if signal[SignalColumns.BUY] == True:
                low = data.loc[prev_reverse_signal.name : signal.name][self.quote].min()
                high = data.loc[prev_same_signal.name : signal.name][self.quote].max()
                delta[i] = (high - low) * self.retracement
            else:
                high = data.loc[prev_reverse_signal.name : signal.name][self.quote].max()
                low = data.loc[prev_same_signal.name : signal.name][self.quote].min()
                delta[i] = -((high - low) * self.retracement)
        stop_profit = signals[self.quote].add(delta)
        return stop_profit.rename(SignalColumns.STOP_PROFIT)
            

    def calc_stop_loss(self, quote_series: pd.Series, buy_idcs: pd.Series, sell_idcs: pd.Series, delta: int) -> pd.Series:
        stop_loss = quote_series - delta*buy_idcs + delta*sell_idcs
        return stop_loss.rename(SignalColumns.STOP_LOSS)


    def __repr__(self):
        return "fibonacci_{}_{}_{}".format(round(self.retracement*100), self.stop_loss, self.quote)


    def __str__(self):
        return "fibonacci_{}_{}_{}".format(round(self.retracement*100), self.stop_loss, self.quote)
