from types import SimpleNamespace
from cli.config_file.parse_argument import parse_arg
from cli.date_validator import valid_date

SUPPORTED_CURRENCY_PAIRS = ['eurusd']


def parse_general_args(config_module) -> SimpleNamespace:
    currency_pair = parse_arg(config_module.CURRENCY_PAIR, 'currency_pair', valid_currency_pair, required=True)
    start = parse_arg(config_module.START, '--start', valid_date)
    stop = parse_arg(config_module.STOP, '--stop', valid_date)
    quote = parse_arg(config_module.QUOTE, '--quote', type=str, required=True)
    no_cache = parse_arg(config_module.NO_CACHE, '--no_cache', type=bool)
    ignore_reverse = parse_arg(config_module.IGNORE_REVERSE, '--ignore_reverse', type=bool)
    
    return SimpleNamespace(
        currency_pair=currency_pair,
        start=start,
        stop=stop,
        quote=quote,
        no_cache=no_cache,
        ignore_reverse=ignore_reverse)


def valid_currency_pair(currency_pair: str) -> str:
    if not currency_pair in SUPPORTED_CURRENCY_PAIRS:
        raise ValueError()
    return currency_pair