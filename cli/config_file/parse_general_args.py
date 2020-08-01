from types import SimpleNamespace
from cli.config_file.parse_argument import parse_arg
from cli.date_validator import valid_date

SUPPORTED_CURRENCY_PAIRS = ['eurusd']
SUPPORTED_TICK_RATES = ['min', 'hour', 'day']


def parse_general_args(config_module) -> SimpleNamespace:
    currency_pair = parse_arg(config_module.CURRENCY_PAIR, 'currency_pair', valid_currency_pair, required=True)
    tick_rate = parse_arg(config_module.TICK_RATE, '--tick_rate', valid_tick_rate) if hasattr(config_module, 'TICK_RATE') else None
    start = parse_arg(config_module.START, '--start', valid_date) if hasattr(config_module, 'START') else None
    stop = parse_arg(config_module.STOP, '--stop', valid_date) if hasattr(config_module, 'STOP') else None
    quote = parse_arg(config_module.QUOTE, '--quote', type=str, required=True)
    no_cache = parse_arg(config_module.NO_CACHE, '--no_cache', type=bool) if hasattr(config_module, 'NO_CACHE') else False
    reverse = parse_arg(config_module.REVERSE, '--reverse', type=bool) if hasattr(config_module, 'REVERSE') else False
    
    return SimpleNamespace(
        currency_pair=currency_pair,
        tick_rate=tick_rate,
        start=start,
        stop=stop,
        quote=quote,
        no_cache=no_cache,
        reverse=reverse)


def valid_currency_pair(currency_pair: str) -> str:
    if not currency_pair in SUPPORTED_CURRENCY_PAIRS:
        raise ValueError()
    return currency_pair


def valid_tick_rate(tick_rate: str) -> int:
    if not tick_rate in SUPPORTED_TICK_RATES:
        raise ValueError()
    return tick_rate