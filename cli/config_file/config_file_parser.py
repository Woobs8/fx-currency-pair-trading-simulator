from types import SimpleNamespace
import imp
from argparse import Namespace
from cli.config_file.signal_strat.parse_signal_strat_args import parse_signal_strat_args
from cli.config_file.stopping_strat.parse_stopping_strat_args import parse_stop_strat_args
from cli.config_file.parse_general_args import parse_general_args


def parse_config_file(fp: str) -> SimpleNamespace:
    config_module = imp.load_source('config', fp)
    general_args = parse_general_args(config_module)
    signal_strat_args = parse_signal_strat_args(config_module)
    stop_strat_args = parse_stop_strat_args(config_module)
    return Namespace(**vars(general_args), **vars(signal_strat_args), **vars(stop_strat_args))



