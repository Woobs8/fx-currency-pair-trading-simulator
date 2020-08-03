from types import SimpleNamespace
from argparse import Namespace
from cli.config_file.parse_argument import parse_arg


STOPPING_STRATEGIES = ['offset', 'fib']


def parse_stop_strat_args(config_module) -> SimpleNamespace:
    stop_strat = parse_arg(config_module.STOPPING_STRAT, 'stopping_strat', type=valid_stopping_strat, required=True)
    if stop_strat == 'offset':
        stop_strat_namespace = parse_offset_stop_strat_args(config_module)
    elif stop_strat == 'fib':
        stop_strat_namespace = parse_fibonacci_stop_strat_args(config_module)
    else:
        raise ValueError("config error 'stopping_strat': invalid value '{}'".format(stop_strat))
    return Namespace(**vars(stop_strat_namespace), **vars(SimpleNamespace(stopping_strat=stop_strat)))


def valid_stopping_strat(stop_strat: str) -> str:
    if not stop_strat in STOPPING_STRATEGIES:
        raise ValueError()
    return stop_strat


def parse_offset_stop_strat_args(config_module) -> SimpleNamespace:
    stop_profit = parse_arg(config_module.STOP_PROFIT, '--stop_profit', type=float, required=True)
    stop_loss = parse_arg(config_module.STOP_LOSS, '--stop_loss', type=float, required=True)
    return SimpleNamespace(stop_profit=stop_profit, stop_loss=stop_loss)


def parse_fibonacci_stop_strat_args(config_module) -> int:
    retracement = parse_arg(config_module.RETRACEMENT, '--retracement', type=float, required=True)
    stop_loss = parse_arg(config_module.STOP_LOSS, '--stop_loss', type=float, required=True)
    margin = parse_arg(config_module.MARGIN, '--margin', type=float, required=True)
    return SimpleNamespace(retracement=retracement, stop_loss=stop_loss, margin=margin)