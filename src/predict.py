import os
import re
import joblib
import numpy as np
import pandas as pd
from .logger import create_logger
from .ml_utils import fetch_daily_ohlcv
from .agent_api import submit_prediction

agent_base_url = os.getenv('ALPHASEA_AGENT_BASE_URL')
model_id = os.getenv('ALPHASEA_MODEL_ID')
model_path = os.getenv('ALPHASEA_MODEL_PATH')
log_level = os.getenv('ALPHASEA_LOG_LEVEL')
symbols = os.getenv('ALPHASEA_SYMBOLS').split(',')
position_noise = float(os.getenv('ALPHASEA_POSITION_NOISE'))

if not re.match(r'^[a-z_][a-z0-9_]{3,30}$', model_id):
    raise Exception('model_id must be ^[a-zA-Z_][a-zA-Z0-9_]{3,30}$')


def predict_job():
    logger = create_logger(log_level)

    # fetch features
    df = fetch_daily_ohlcv(symbols=symbols, logger=logger)

    # predict
    model = joblib.load(model_path)
    df['y_pred'] = model.predict(df)

    # calc position
    df['position'] = np.sign(df['y_pred'])
    df['position'] += np.random.normal(0, position_noise, size=df.shape[0])

    # normalize
    df['position_abs'] = df['position'].abs()
    df['position'] /= 1e-37 + df.groupby('timestamp')['position_abs'].transform('sum')

    # filter last timestamp
    df = df.loc[df.index.get_level_values('timestamp') == df.index.get_level_values('timestamp').max()]

    # submit
    result = submit_prediction(
        agent_base_url=agent_base_url,
        model_id=model_id,
        df=df,
        prediction_license='CC0-1.0'
    )
    logger.info(result)
