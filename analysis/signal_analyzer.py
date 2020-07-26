import pandas as pd
from analysis.signal_resolver import SignalResolver
from analysis.signal_types import SignalTypes
from analysis.closing_causes import ClosingCauses
from shared.columns import ResolvedSignalColumns

class SignalAnalyzer:

    def __init__(self, resolved_signals: pd.DataFrame):
        self.resolved_signals = resolved_signals


    def get_stats(self, start_year: int = None, stop_year: int = None) -> dict:
        buy_stats = self.get_buy_stats(start_year, stop_year)
        sell_stats = self.get_sell_stats(start_year, stop_year)
        return {'buy': buy_stats, 'sell': sell_stats}


    def get_buy_stats(self, start_year: int = None, stop_year: int = None) -> dict:
        buy_signals = self.resolved_signals[self.resolved_signals[ResolvedSignalColumns.TYPE] == SignalTypes.BUY]
        buy_signals = self.filter_between_years(buy_signals, start_year, stop_year)
        return self.calc_signals_stats(buy_signals)


    def filter_between_years(self, signals: pd.DataFrame, start_year: int = None, stop_year: int = None):
        if start_year is not None:
            signals = signals[signals[ResolvedSignalColumns.OPEN].dt.year >= year]
        if stop_year is not None:
            signals = signals[signals[ResolvedSignalColumns.OPEN].dt.year <= year]
        return signals
    
    def get_sell_stats(self, start_year: int = None, stop_year: int = None) -> dict:
        sell_signals = self.resolved_signals[self.resolved_signals[ResolvedSignalColumns.TYPE] == SignalTypes.SELL]
        sell_signals = self.filter_between_years(sell_signals, start_year, stop_year)
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

