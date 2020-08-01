import pandas as pd
from datetime import datetime
from .signal_resolver import SignalResolver
from .closing_causes import ClosingCauses
from .signal_types import SignalTypes
from .utils import filter_between_years
from shared import ResolvedSignalColumns

class SignalAnalyzer:

    def __init__(self, resolved_signals: pd.DataFrame):
        self.resolved_signals = resolved_signals


    def get_stats(self, start: datetime = None, stop: datetime = None) -> dict:
        buy_stats = self.get_buy_stats(start, stop)
        sell_stats = self.get_sell_stats(start, stop)
        total_count = buy_stats['count'] + sell_stats['count']
        return {'start': start, 'stop': stop, 'count': total_count, 'buy': buy_stats, 'sell': sell_stats}


    def get_buy_stats(self, start: datetime = None, stop: datetime = None) -> dict:
        buy_signals = self.resolved_signals[self.resolved_signals[ResolvedSignalColumns.TYPE] == SignalTypes.BUY]
        buy_signals = filter_between_years(buy_signals, start, stop, ResolvedSignalColumns.OPEN)
        return self.calc_signals_stats(buy_signals)
    

    def get_sell_stats(self, start: datetime = None, stop: datetime = None) -> dict:
        sell_signals = self.resolved_signals[self.resolved_signals[ResolvedSignalColumns.TYPE] == SignalTypes.SELL]
        sell_signals = filter_between_years(sell_signals, start, stop, ResolvedSignalColumns.OPEN)
        return self.calc_signals_stats(sell_signals)


    def calc_signals_stats(self, signals: pd.DataFrame) -> dict:
        count = len(signals.index)
        net_gain_stats = self.calc_normal_distribution(signals[ResolvedSignalColumns.NET_GAIN])
        duration = signals[ResolvedSignalColumns.CLOSE] - signals[ResolvedSignalColumns.OPEN] 
        duration_stats = self.calc_normal_distribution(duration)
        closing_cause_count = signals[ResolvedSignalColumns.CAUSE].value_counts().to_dict()
        closing_cause_count = {ClosingCauses(k).name:v for k, v in closing_cause_count.items()}
        return {'count': count, 'net_gain': net_gain_stats, 'duration': duration_stats, 'closings': closing_cause_count}


    def calc_normal_distribution(self, data: pd.Series) -> dict:
        mean = data.mean()
        std = data.std()
        return {'mean': mean, 'std': std}

