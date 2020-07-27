import pandas as pd
from caching.cache import Cache
from analysis.closing_causes import ClosingCauses
from analysis.signal_types import SignalTypes
from shared.columns import SourceDataColumns as sourcecol, SignalColumns as sigcol, ResolvedSignalColumns as ressigcol
from datetime import datetime
import hashlib

class SignalResolver:

    def __init__(self, data_series: pd.Series, ignore_reverse: bool = False):
        self.data_series = data_series
        self.ignore_reverse = ignore_reverse
        self.columns = [ressigcol.OPEN, ressigcol.OPEN_QUOTE, ressigcol.TYPE, ressigcol.STOP_PROFIT, ressigcol.STOP_LOSS, ressigcol.CLOSE, ressigcol.NET_GAIN, ressigcol.CAUSE]


    def get_resolve_signals(self, signals: pd.DataFrame) -> pd.DataFrame:
        signals_hash = hashlib.sha1(pd.util.hash_pandas_object(signals).values).hexdigest()
        cache_key = 'k{}_{}'.format(signals_hash, self.ignore_reverse)
        cache = Cache.get()
        if cache.cache_exists and cache.contains(cache_key):
            print('Loading resolved signals for [{}] from cache.'.format(cache_key))
            resolved_signals = cache.fetch(cache_key)
        else:
            resolved_signals = self.resolve_signals(signals)
            print('Caching result for [{}].'.format(cache_key))
            cache.put(resolved_signals, cache_key)
        return resolved_signals


    def resolve_signals(self, signals: pd.DataFrame) -> pd.DataFrame:
        resolved_positions = []
        for i, signal in enumerate(signals.itertuples()):
            if i < (signals.shape[0] - 1):
                if self.ignore_reverse:
                    next_index = signals.shape[0] - 1
                else:
                    next_index = i + 1
            else:
                break
            signal_reverse_time = signals.iloc[next_index,:].name
            resolved_positions.append(self.resolve_position(signal, signal_reverse_time))
        return pd.DataFrame(resolved_positions)

    
    def resolve_position(self, signal: pd.Series, reversed_at: datetime) -> pd.Series:
        opened_at = getattr(signal, 'Index').to_pydatetime()
        stop_profit = getattr(signal, sigcol.STOP_PROFIT)
        stop_loss = getattr(signal, sigcol.STOP_LOSS)
        signal_type = SignalTypes.BUY if getattr(signal, sigcol.BUY) else SignalTypes.SELL
        opening_quote = self.data_series.loc[opened_at]
        position_window = self.get_position_window(opened_at, reversed_at)

        if signal_type == SignalTypes.BUY:
            take_profit_at, take_loss_at = self.find_buy_exits(position_window, stop_profit, stop_loss)
        else:
            take_profit_at, take_loss_at = self.find_sell_exits(position_window, stop_profit, stop_loss) 

        if take_profit_at is not None and take_loss_at is not None:
            if take_profit_at <= take_loss_at:
                closing_quote = position_window.loc[take_profit_at]
                closing_time = take_profit_at
                cause = ClosingCauses.STOP_PROFIT
            else:
                closing_quote = position_window.loc[take_loss_at]
                closing_time = take_loss_at
                cause = ClosingCauses.STOP_LOSS
        elif take_profit_at is not None:
            closing_quote = position_window.loc[take_profit_at]
            closing_time = take_profit_at
            cause = ClosingCauses.STOP_PROFIT
        elif take_loss_at is not None:
            closing_quote = position_window.loc[take_loss_at]
            closing_time = take_loss_at
            cause = ClosingCauses.STOP_LOSS
        else:
            closing_quote = position_window.iloc[-1]
            closing_time = position_window.index[-1].to_pydatetime()
            cause = ClosingCauses.REVERSE_SIGNAL
        
        if signal_type == SignalTypes.BUY:
            net_pips_gain = closing_quote - opening_quote
        else:
            net_pips_gain = opening_quote - closing_quote

        return pd.Series([opened_at, opening_quote, signal_type, stop_profit, stop_loss, closing_time, net_pips_gain, cause], index=self.columns)


    def get_position_window(self, opened_at: datetime, closed_at: datetime) -> pd.DataFrame:
        return self.data_series.loc[opened_at:closed_at]


    def find_buy_exits(self, window: pd.Series, stop_profit: float, stop_loss: float) -> (int, int):
        take_profit_index = window[(window >= stop_profit).values].first_valid_index()
        take_loss_index = window[(window <= stop_loss).values].first_valid_index()
        return take_profit_index, take_loss_index

    
    def find_sell_exits(self, window: pd.Series, stop_profit: float, stop_loss: float) -> (int, int):
        take_profit_index = window[(window <= stop_profit).values].first_valid_index()
        take_loss_index = window[(window >= stop_loss).values].first_valid_index()
        return take_profit_index, take_loss_index
