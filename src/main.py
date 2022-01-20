import time
import schedule
from .predict import predict_job

# check at startup
predict_job(dry_run=True)

schedule.every().day.at('00:04').do(predict_job)

while True:
    schedule.run_pending()
    time.sleep(1)
