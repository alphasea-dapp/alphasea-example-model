import os
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


def main():
    logger = create_logger(log_level)

    # fetch features
    df = fetch_daily_ohlcv(symbols=symbols, logger=logger)

    # predict
    model = joblib.load(model_path)
    df['y_pred'] = model.predict(df)

    # calc position
    df['position'] = np.sign(df['y_pred'])
    df['position_abs'] = df['position'].abs()
    df['position'] /= 1e-37 + df.groupby('timestamp')['position'].transform('sum')

    # filter last timestamp
    df = df.loc[df.index.get_level_values('timestamp') == df.index.get_level_values('timestamp').max()]

    # submit
    result = submit_prediction(
        agent_base_url=agent_base_url,
        model_id=model_id,
        df=df
    )
    logger.info(result)


main()
