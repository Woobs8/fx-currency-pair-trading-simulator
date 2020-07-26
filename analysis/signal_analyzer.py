import pandas as pd
from analysis.signal_resolver import SignalResolver
from analysis.signal_types import SignalTypes
from analysis.closing_causes import ClosingCauses
from shared.columns import ResolvedSignalColumns

class SignalAnalyzer:

    def __init__(self, data_series: pd.DataFrame, signals: pd.DataFrame, ignore_reverse: bool = False):
        self.data_series = data_series
        self.signals = signals
        self.ignore_reverse = ignore_reverse
        self.resolver = SignalResolver(self.data_series, ignore_reverse)
        self.resolved_signals = self.resolver.resolve_signals(self.signals)


    def get_resolved_signals(self, year: int = None) -> pd.DataFrame:
        if year is not None:
            return resolved_signals[resolved_signals[ResolvedSignalColumns.OPEN].dt.year == year]
        return self.resolved_signals


    def get_stats(self, year: int = None) -> dict:
        buy_stats = self.get_buy_stats(year)
        sell_stats = self.get_sell_stats(year)
        return {'buy': buy_stats, 'sell': sell_stats}


    def get_buy_stats(self, year: int = None) -> dict:
        buy_signals = self.resolved_signals[self.resolved_signals[ResolvedSignalColumns.TYPE] == SignalTypes.BUY]
        if year is not None:
            buy_signals = buy_signals[buy_signals[ResolvedSignalColumns.OPEN].dt.year == year]
        return self.calc_signals_stats(buy_signals)

    
    def get_sell_stats(self, year: int = None) -> dict:
        sell_signals = self.resolved_signals[self.resolved_signals[ResolvedSignalColumns.TYPE] == SignalTypes.SELL]
        if year is not None:
            sell_signals = sell_signals[sell_signals[ResolvedSignalColumns.OPEN].dt.year == year]
        return self.calc_signals_stats(sell_signals)


    def calc_signals_stats(self, signals: pd.DataFrame) -> dict:
        net_gain_stats = self.calc_normal_distribution(signals[ResolvedSignalColumns.NET_GAIN])
        duration = signals[ResolvedSignalColumns.CLOSE] - signals[ResolvedSignalColumns.OPEN] 
        duration_stats = self.calc_normal_distribution(duration)
        closing_cause_count = signals[ResolvedSignalColumns.CAUSE].value_counts()
        return {'net_gain': net_gain_stats, 'duration': duration_stats, 'closings': closing_cause_count.to_dict()}


    def calc_normal_distribution(self, data: pd.Series) -> dict:
        mean = data.mean()
        std = data.std()
        return {'mean': mean, 'std': std}

