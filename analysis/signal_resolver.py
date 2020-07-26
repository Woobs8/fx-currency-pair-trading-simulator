import pandas as pd
from analysis.closing_causes import ClosingCauses
from analysis.signal_types import SignalTypes
from shared.columns import SourceDataColumns as sourcecol, SignalColumns as sigcol, ResolvedSignalColumns as ressigcol
from datetime import datetime

class SignalResolver:

    def __init__(self, data_series: pd.DataFrame):
        self.data_series = data_series
        self.columns = [ressigcol.OPEN, ressigcol.OPEN_QUOTE, ressigcol.TYPE, ressigcol.STOP_PROFIT, ressigcol.STOP_LOSS, ressigcol.CLOSE, ressigcol.NET_GAIN, ressigcol.CAUSE]
    

    def resolve_signals(self, signals: pd.DataFrame) -> pd.DataFrame:
        resolved_positions = []
        for i, signal in enumerate(signals.itertuples()):
            next_index = i + 1
            if next_index < signals.shape[0]:
                signal_reverse_time = signals.iloc[next_index,:].name
                resolved_positions.append(self.resolve_position(signal, signal_reverse_time))
        return pd.DataFrame(resolved_positions)

    
    def resolve_position(self, signal: pd.Series, reversed_at: datetime) -> pd.Series:
        opened_at = getattr(signal, 'Index').to_pydatetime()
        stop_profit = getattr(signal, sigcol.STOP_PROFIT)
        stop_loss = getattr(signal, sigcol.STOP_LOSS)
        signal_type = SignalTypes.BUY if getattr(signal, sigcol.BUY) else SignalTypes.SELL
        opening_quote = self.data_series.loc[opened_at][sourcecol.QUOTE_OPEN]
        position_window = self.get_position_window(opened_at, reversed_at)

        if signal_type == SignalTypes.BUY:
            take_profit_index, take_loss_index = self.find_buy_exits(position_window, stop_profit, stop_loss)
        else:
            take_profit_index, take_loss_index = self.find_sell_exits(position_window, stop_profit, stop_loss) 

        take_profit_at =  position_window.loc[take_profit_index, :].name if take_profit_index is not None else None
        take_loss_at = position_window.loc[take_loss_index, :].name if take_loss_index is not None else None

        if take_profit_at is not None and take_loss_at is not None:
            if take_profit_at <= take_loss_at:
                closing_quote = position_window.loc[take_profit_index, :][sourcecol.QUOTE_OPEN]
                closing_time = take_profit_at
                cause = ClosingCauses.STOP_PROFIT
            else:
                closing_quote = position_window.loc[take_loss_index, :][sourcecol.QUOTE_OPEN]
                closing_time = take_loss_at
                cause = ClosingCauses.STOP_LOSS
        elif take_profit_at is not None:
            closing_quote = position_window.loc[take_profit_index, :][sourcecol.QUOTE_OPEN]
            closing_time = take_profit_at
            cause = ClosingCauses.STOP_PROFIT
        elif take_loss_at is not None:
            closing_quote = position_window.loc[take_loss_index, :][sourcecol.QUOTE_OPEN]
            closing_time = take_loss_at
            cause = ClosingCauses.STOP_LOSS
        else:
            closing_quote = position_window.tail(1)[sourcecol.QUOTE_OPEN]
            closing_time = position_window.index[-1].to_pydatetime()
            cause = ClosingCauses.REVERSE_SIGNAL
        
        if signal_type == SignalTypes.BUY:
            net_pips_gain = closing_quote - opening_quote
        else:
            net_pips_gain = opening_quote - closing_quote
        return pd.Series([opened_at, opening_quote, signal_type, stop_profit, stop_loss, closing_time, net_pips_gain, cause], index=self.columns)


    def get_position_window(self, opened_at: datetime, closed_at: datetime) -> pd.DataFrame:
        return self.data_series.loc[opened_at:closed_at]


    def find_buy_exits(self, window: pd.DataFrame, stop_profit: float, stop_loss: float) -> (int, int):
        take_profit_index = window[(window[sourcecol.QUOTE_OPEN] >= stop_profit).values].first_valid_index()
        take_loss_index = window[(window[sourcecol.QUOTE_OPEN] <= stop_loss).values].first_valid_index()
        return take_profit_index, take_loss_index

    
    def find_sell_exits(self, window: pd.DataFrame, stop_profit: float, stop_loss: float) -> (int, int):
        take_profit_index = window[(window[sourcecol.QUOTE_OPEN] <= stop_profit).values].first_valid_index()
        take_loss_index = window[(window[sourcecol.QUOTE_OPEN] >= stop_loss).values].first_valid_index()
        return take_profit_index, take_loss_index
