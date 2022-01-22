import os
import re
import joblib
import numpy as np
import pandas as pd
from .logger import create_logger
from .ml_utils import fetch_ohlcv, normalize_position
from .agent_api import submit_prediction

agent_base_url = os.getenv('ALPHASEA_AGENT_BASE_URL')
model_id_prefix = os.getenv('ALPHASEA_MODEL_ID_PREFIX')
model_path = os.getenv('ALPHASEA_MODEL_PATH')
log_level = os.getenv('ALPHASEA_LOG_LEVEL')
symbols = os.getenv('ALPHASEA_SYMBOLS').split(',')
position_noise = float(os.getenv('ALPHASEA_POSITION_NOISE'))

if not re.match(r'^[a-z_][a-z0-9_]{3,30}$', model_id_prefix):
    raise Exception('model_id must be ^[a-z_][a-z0-9_]{3,30}$')


def predict_job(dry_run=False):
    logger = create_logger(log_level)
    model = joblib.load(model_path)

    # fetch data
    interval_sec = 60 * 60
    df = fetch_ohlcv(symbols=symbols, logger=logger, interval_sec=interval_sec)
    max_timestamp = df.index.get_level_values('timestamp').max()
    df = df.loc[max_timestamp - pd.to_timedelta(model.max_data_sec, unit='S') <= df.index.get_level_values('timestamp')]

    # predict
    df['position'] = model.predict(df)

    # add noise (for debug)
    df['position'] += np.random.normal(0, position_noise, size=df.shape[0])
    normalize_position(df)

    # filter last timestamp
    df = df.loc[df.index.get_level_values('timestamp') == max_timestamp]

    # submit
    if dry_run:
        logger.info('dry run submit {}'.format(df))
    else:
        result = submit_prediction(
            agent_base_url=agent_base_url,
            model_id_prefix=model_id_prefix,
            df=df,
            prediction_license='CC0-1.0'
        )
        logger.info(result)
