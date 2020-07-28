from types import SimpleNamespace
from cli.config_file.parse_argument import parse_arg


MA_FUNCTIONS = ['ema', 'sma']


def parse_signal_strat_args(config_module) -> SimpleNamespace:
    ma = parse_arg(config_module.MA_FNC, '--ma', type=valid_ma_fnc, required=True)
    short_window = parse_arg(config_module.SHORT_WINDOW, '--short', type=int, required=True)
    long_window = parse_arg(config_module.LONG_WINDOW, '--long', type=int, required=True)
    delta = parse_arg(config_module.DELTA, '--delta', type=int, required=True)
    return SimpleNamespace(
        ma=ma,
        short=short_window,
        long=long_window,
        delta=delta)


def valid_ma_fnc(ma_fnc: str) -> str:
    if not ma_fnc in MA_FUNCTIONS:
        raise ValueError()
    return ma_fnc

