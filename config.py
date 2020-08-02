# GENERAL
CURRENCY_PAIR = 'eurusd'
TICK_RATE = 'hour' # min / hour / day
START = '2018-01-01' #YYYY-mm-dd
#STOP = '2019-01-01' #YYYY-mm-dd
QUOTE = 'open' # open / close / high / low
NO_CACHE = False


# SIGNAL DETECTION
MA_FNC = 'ema' # ema / sma
SHORT_WINDOW = 12 # ticks
LONG_WINDOW = 24 # ticks
DELTA = 5 # pips
CONFIDENCE_WINDOW = 3 # ticks


# STOPPING CRITERIA
STOPPING_STRAT = 'fib' # offset / fib
#STOP_PROFIT = 100 # pips
RETRACEMENT = 0.5
STOP_LOSS = 50 # pips


# SIGNAL RESOLVING
REVERSE = False

