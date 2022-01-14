from unittest import TestCase
from src.predict import predict_job


class TestPredictJob(TestCase):
    def test_smoke(self):
        predict_job()

