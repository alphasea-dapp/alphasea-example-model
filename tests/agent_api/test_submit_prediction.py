from unittest import TestCase
import os
import pandas as pd
from src.agent_api import submit_prediction


class TestSubmitPrediction(TestCase):
    def test_ok(self):
        agent_base_url = os.getenv('ALPHASEA_AGENT_BASE_URL')

        df = pd.DataFrame([
            ['BTC', 0.1]
        ], columns=['symbol', 'position']).set_index('symbol')
        df['execution_start_at'] = pd.to_datetime('2020-01-01 0:30Z')

        result = submit_prediction(
            agent_base_url=agent_base_url,
            model_id='model1',
            df=df,
            prediction_license='CC0-1.0'
        )
        self.assertEqual(result, {})

