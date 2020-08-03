from .stopping_strategy import StoppingStrategy
from shared import SourceDataColumns, SignalColumns
import pandas as pd
from tqdm import tqdm
import numpy as np


class FibonacciStoppingStrategy(StoppingStrategy):

    def __init__(self, retracement: float, margin: float, stop_loss: int, quote: str):
        self.retracement = retracement
        self.margin = margin
        self.stop_loss = stop_loss
        self.quote = quote
        super().__init__()


    def find_stopping_criteria(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        quotes = pd.merge(data, signals, left_index=True, right_index=True)
        buy_indices = (quotes[SignalColumns.BUY] == True).values
        sell_indices = (quotes[SignalColumns.SELL] == True).values
        stop_loss_criteria = self.calc_stop_loss(quotes[self.quote], buy_indices, sell_indices, self.stop_loss)
        stop_profit_criteria = self.calc_stop_profit(quotes, data)
        stopping_criteria = pd.merge(stop_profit_criteria, stop_loss_criteria, left_index=True, right_index=True).dropna()
        return stopping_criteria


    def calc_stop_profit(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.Series:
        stop_profit = [None] * signals.shape[0]
        progress = tqdm(range(len(stop_profit)))
        progress.set_description('Calculating stopping criteria')
        for i in progress:
            signal = signals.iloc[i,:]
            window_until_signal = signals.iloc[:i, :]
            prev_reverse_signal = self.find_last_reverse_signal_in_window(signal, window_until_signal)
            
            if prev_reverse_signal is not None:
                window_until_prev_reverse_signal = window_until_signal.loc[window_until_signal.index < prev_reverse_signal.name]
                prev_same_signal = self.find_last_same_signal_in_window(signal, window_until_prev_reverse_signal)
            else:
                prev_same_signal = None

            if prev_reverse_signal is not None and prev_same_signal is not None:
                if signal[SignalColumns.BUY] == True:
                    stop_profit[i] = self.calc_buy_retracement(data, signal, prev_reverse_signal, prev_same_signal)
                else:
                    stop_profit[i] = self.calc_sell_retracement(data, signal, prev_reverse_signal, prev_same_signal)
        return pd.Series(stop_profit, index=signals.index).rename(SignalColumns.STOP_PROFIT)
    

    def find_last_reverse_signal_in_window(self, signal: pd.Series, window: pd.DataFrame) -> pd.Series:
        prev_reverse_signal_index = (window[SignalColumns.BUY] != signal[SignalColumns.BUY]).last_valid_index()
        if prev_reverse_signal_index is not None:
            return window.loc[prev_reverse_signal_index]
        else:
            return None


    def find_last_same_signal_in_window(self, signal: pd.Series, window: pd.DataFrame) -> pd.Series:
        prev_same_signal_index = (window[SignalColumns.BUY] == signal[SignalColumns.BUY]).last_valid_index()
        if prev_same_signal_index is not None:
            return window.loc[prev_same_signal_index]
        else:
            return None


    def calc_buy_retracement(self, data: pd.DataFrame, signal: pd.Series, prev_reverse_signal: pd.Series, prev_same_signal: pd.Series) -> float:
        high_idx = data.loc[prev_same_signal.name : signal.name][SourceDataColumns.QUOTE_HIGH].idxmax()
        high = data.loc[high_idx][SourceDataColumns.QUOTE_HIGH]
        low = data.loc[high_idx : signal.name][SourceDataColumns.QUOTE_LOW].min()
        retrace = low + (high - low) * self.retracement
        return retrace if retrace > (signal[self.quote] + self.margin) else None


    def calc_sell_retracement(self, data: pd.DataFrame, signal: pd.Series, prev_reverse_signal: pd.Series, prev_same_signal: pd.Series) -> float:
        low_idx = data.loc[prev_same_signal.name : signal.name][SourceDataColumns.QUOTE_LOW].idxmin()
        low = data.loc[low_idx][SourceDataColumns.QUOTE_LOW]
        high = data.loc[low_idx : signal.name][SourceDataColumns.QUOTE_HIGH].max()
        retrace = high - ((high - low) * self.retracement)
        return retrace if retrace < (signal[self.quote] - self.margin) else None



    def calc_stop_loss(self, quote_series: pd.Series, buy_idcs: pd.Series, sell_idcs: pd.Series, delta: int) -> pd.Series:
        stop_loss = quote_series - delta*buy_idcs + delta*sell_idcs
        return stop_loss.rename(SignalColumns.STOP_LOSS)


    def __repr__(self):
        return "(retracement:{:.2f}, margin:{:.6f}, stop_loss:{:.6f}, quote:{})".format(self.retracement, self.margin, self.stop_loss, self.quote)


    def __str__(self):
        return "FibonacciStoppingStrategy(retracement={:.2f}, margin={:.6f}, stop_loss={:.6f}, quote={})".format(self.retracement, self.margin, self.stop_loss, self.quote)
