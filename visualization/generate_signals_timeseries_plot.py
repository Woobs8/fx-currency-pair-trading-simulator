import plotly.graph_objects as go
import pandas as pd
from shared import SourceDataColumns, MovingAverageColumns, ResolvedSignalColumns
from analysis import SignalTypes, ClosingCauses
from utils.fileutils import get_output_dir
from os import path, makedirs
from tqdm import tqdm
from datetime import datetime
from utils.timezone import get_local_timezone


def generate_signals_timeseries_plot(data: pd.Series, resolved_signals: pd.DataFrame, moving_averages: pd.DataFrame, start: datetime = None, stop: datetime = None, simulation_id: str = None):
    output_dir = get_output_dir(simulation_id)
    if not path.exists(output_dir):
        makedirs(output_dir, exist_ok=True)
    data = filter_between_years(data, start, stop)
    resolved_signals = filter_between_years(resolved_signals, start, stop, ResolvedSignalColumns.OPEN)
    moving_averages = filter_between_years(moving_averages, start, stop)
    years = data.index.year.unique()
    print('Preparing signal visualizations for the years {}'.format(years.values))
    progress = tqdm(years)
    for year in progress:
        progress.set_description('Processing {}'.format(year))
        output_fp = '{}/{}_signals.html'.format(output_dir, year)
        plot_signals_series(output_fp, year, data[data.index.year == year], resolved_signals[resolved_signals[ResolvedSignalColumns.OPEN].dt.year == year], moving_averages[moving_averages.index.year == year])



def filter_between_years(df: pd.DataFrame, start: datetime = None, stop: datetime = None, col: str = None) -> pd.DataFrame:    
    if col is not None:
        if start is not None:
            df = df[df[col] >= start]
        if stop is not None:
            df = df[df[col] <= stop]
    else:
        if start is not None:
            df = df.loc[start:]
        if stop is not None:
            df = df.iloc[:stop]
    return df


def plot_signals_series(fp: str, title: str, data: pd.DataFrame, resolved_signals: pd.DataFrame, moving_averages: pd.DataFrame):
    layout = go.Layout(
        title=title,
        xaxis=dict(
            title="Time"
        ),
        yaxis=dict(
            title="Quote"
        )
    )

    fig = go.Figure(layout=layout)
    add_line(data, fig, 'open bid')
    add_line(moving_averages[MovingAverageColumns.SHORT_AVG], fig, 'short')
    add_line(moving_averages[MovingAverageColumns.LONG_AVG], fig, 'long')
    add_signals(resolved_signals, fig)
    fig.write_html(fp)


def add_line(data: pd.Series, fig: go.Figure, name: str):
    fig.add_trace(go.Scattergl(
        x=data.index, 
        y=data,
        mode='lines',
        name=name))


def add_signals(signals: pd.DataFrame, fig: go.Figure):
    for signal in signals.itertuples():
        opened_at = getattr(signal, ResolvedSignalColumns.OPEN)
        closed_at = getattr(signal, ResolvedSignalColumns.CLOSE)
        quote = getattr(signal, ResolvedSignalColumns.OPEN_QUOTE)
        stop_profit = getattr(signal, ResolvedSignalColumns.STOP_PROFIT)
        stop_loss = getattr(signal, ResolvedSignalColumns.STOP_LOSS)
        net_gain = getattr(signal, ResolvedSignalColumns.NET_GAIN)
        sig_type = SignalTypes(getattr(signal, ResolvedSignalColumns.TYPE))
        color = '#208c4f' if sig_type == SignalTypes.BUY else '#ed1f11'
        close_cause = ClosingCauses(getattr(signal, ResolvedSignalColumns.CAUSE))

        hovertext = format_signal_hover_text(sig_type.name, quote, opened_at, closed_at, stop_profit, stop_loss, close_cause.name, net_gain)
        add_annotation(opened_at, quote, sig_type.name, hovertext, color, fig)


def format_signal_hover_text(sig_type: str, 
    quote: float, 
    opened_at: pd.Timestamp, 
    closed_at: pd.Timestamp, 
    stop_profit: float, 
    stop_loss: float,
    close_cause: str, 
    net_gain: float) -> str:
    return """{}
        <br>
        <br>quote: {}
        <br>open: {}
        <br>close: {}
        <br>stop profit: {:.6f}
        <br>stop loss: {:.6f}
        <br>close cause: {}
        <br>net gain: {:.6f}""".format(sig_type, quote, opened_at, closed_at, stop_profit, stop_loss, close_cause, net_gain)


def add_annotation(x: pd.Timestamp, y: float, text: str, hovertext: str, color: str, fig: go.Figure):
    fig.add_annotation(
            x=x,
            y=y,
            text=text,
            align="center",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=color,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color=color
            ),
            hovertext=hovertext)
