from . import init
from caching import Cache
from shared import ResolvedSignalColumns
from preprocessing.datautils import calc_moving_averages
from analysis import SignalResolver, SignalAnalyzer, generate_report
from visualization import generate_signals_distribution_plot, generate_signals_timeseries_plot
import pandas as pd
from argparse import Namespace


def run(args: Namespace):
    data, resampled_data, signals = init(args)
    resolved_signals, stats = simulate(data, signals, args)
    report(stats, args.id)
    generate_plots(resampled_data, signals, resolved_signals, args)
    

def simulate(data: pd.Series, signals: pd.DataFrame, args: Namespace) -> (pd.DataFrame, dict):
    with Cache.configure(args.currency_pair, args.tick_rate):
        resolver = SignalResolver(data[args.quote], args.reverse)
        if args.no_cache:
            resolved_signals = resolver.resolve_signals(signals, args.start, args.stop)
        else:
            resolved_signals = resolver.get_resolve_signals(signals, args.start, args.stop)
        analyzer = SignalAnalyzer(resolved_signals)
        stats = analyzer.get_stats(args.start, args.stop)
        return resolved_signals, stats


def report(simulation_stats: dict, simulation_id: str = None):
    generate_report(simulation_stats, simulation_id)


def generate_plots(data: pd.Series, signals: pd.DataFrame, resolved_signals: pd.DataFrame, args):
    generate_signals_distribution_plot('net_gain_distribution', resolved_signals, ResolvedSignalColumns.NET_GAIN, 0.0001, args.start, args.stop, args.id)
    if args.plot_timeseries:
        moving_averages = calc_moving_averages(data[args.quote], args.ma_fnc, args.short_window, args.long_window)
        generate_signals_timeseries_plot(data[args.quote], resolved_signals, moving_averages, args.start, args.stop, args.id)