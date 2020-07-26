class SourceDataColumns:
    QUOTE_HIGH = 'high'
    QUOTE_LOW = 'low'
    QUOTE_OPEN = 'open'
    QUOTE_CLOSE = 'close'


class MovingAverageColumns:
    SHORT_AVG = 'short'
    LONG_AVG = 'long'


class SignalColumns:
    BUY = 'buy'
    SELL = 'sell'
    STOP_PROFIT = 'stop_profit'
    STOP_LOSS = 'stop_loss'


class ResolvedSignalColumns:
    OPEN = 'opened_at'
    TYPE = 'signal_type'
    OPEN_QUOTE = 'open_quote'
    STOP_PROFIT = 'stop_profit'
    STOP_LOSS = 'stop_loss'
    CLOSE = 'closed_at'
    NET_GAIN = 'net_gain_pips'
    CAUSE = 'cause'