import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from os import path, makedirs
from shared import ResolvedSignalColumns
from utils.fileutils import get_output_dir
from analysis import SignalTypes


def generate_signals_distribution_plot(title: str, signals: pd.DataFrame, col: str, bin_size: int, start: datetime = None, stop: datetime = None, simulation_id: str = None):
    output_dir = get_output_dir(simulation_id)
    if not path.exists(output_dir):
        makedirs(output_dir, exist_ok=True)

    signals = filter_between_years(signals, ResolvedSignalColumns.OPEN, start, stop)
    signal_types = {SignalTypes(type): group for type, group in signals.groupby(ResolvedSignalColumns.TYPE)[col]}
    fig = get_normal_distribution_plot(signal_types, bin_size)
    fig.update_layout(title_text=title)
    output_fp = '{}/{}.html'.format(output_dir, title)
    fig.write_html(output_fp)


def filter_between_years(df: pd.DataFrame, col: str, start: datetime = None, stop: datetime = None) -> pd.DataFrame:    
    if start is not None:
        df = df[df[col] >= start]
    if stop is not None:
        df = df[df[col] <= stop]
    return df


def get_normal_distribution_plot(datasets: dict, bin_size: float) -> go.Figure:
    labels = list(datasets.keys())
    data = [datasets[key] for key in labels]
    return ff.create_distplot(data, group_labels=labels, bin_size=bin_size, curve_type='normal')