import ccxt
from ccxt_rate_limiter import scale_limits, wrap_object
from ccxt_rate_limiter.ftx import ftx_limits, ftx_wrap_defs
from ccxt_rate_limiter.rate_limiter_group import RateLimiterGroup
from crypto_data_fetcher.ftx import FtxFetcher
import pandas as pd


def fetch_daily_ohlcv(symbols: list, with_target=False, logger=None):
    dfs = []
    for symbol in symbols:
        fetcher = create_data_fetcher(logger=logger)
        df = fetcher.fetch_ohlcv(
            df=None,
            start_time=None,
            interval_sec=24 * 60 * 60,
            market=symbol + '-PERP',
            price_type='index'
        )
        df = df.reset_index()

        df['symbol'] = symbol
        df['execution_start_at'] = df['timestamp'] + pd.to_timedelta(24 * 60 * 60 + 30 * 60, unit='S')
        df = df.set_index(['timestamp', 'symbol'])
        dfs.append(df)
    df = pd.concat(dfs)

    if with_target:
        df_target = _fetch_targets(symbols=symbols, logger=logger)
        df = df.reset_index().merge(df_target.reset_index(), on=['symbol', 'execution_start_at'], how='left')
        df = df.set_index(['timestamp', 'symbol'])

    df = df.sort_index()
    return df


def _fetch_targets(symbols: list, logger=None):
    dfs = []
    for symbol in symbols:
        fetcher = create_data_fetcher(logger=logger)
        df = fetcher.fetch_ohlcv(
            df=None,
            start_time=None,
            interval_sec=300,
            market=symbol + '-PERP',
            price_type='index'
        )

        df = df.reset_index()

        shift = pd.to_timedelta(30 * 60, unit='S')
        df['execution_start_at'] = (df['timestamp'] - shift).dt.floor('1H') + shift
        df = pd.concat([
            df.groupby(['execution_start_at'])['cl'].mean().rename('twap'),
        ], axis=1)
        df['ret'] = df['twap'].shift(-24) / df['twap'] - 1
        df = df.drop(columns='twap')
        df = df.dropna()

        df = df.reset_index()
        df['symbol'] = symbol
        df = df.set_index(['execution_start_at', 'symbol'])

        dfs.append(df)

    df = pd.concat(dfs)
    return df


def create_data_fetcher(logger=None):
    ftx_rate_limiter = RateLimiterGroup(limits=scale_limits(ftx_limits(), 0.5))
    client = ccxt.ftx({
        'enableRateLimit': False,
    })
    wrap_object(
        client,
        rate_limiter_group=ftx_rate_limiter,
        wrap_defs=ftx_wrap_defs()
    )
    return FtxFetcher(ccxt_client=client, logger=logger)


def unbiased_rank2(x):
    count = x.transform('count')
    rank = x.rank()
    return (rank - 1.0).mask(count == 1, rank - 0.5) / (count - 1.0).mask(count == 1, 1.0)
