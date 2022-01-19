import time
import schedule
from .predict import predict_job

schedule.every().day.at('00:04').do(predict_job)

while True:
    schedule.run_pending()
    time.sleep(1)
