import time
import schedule
from .predict import predict_job

# check at startup
predict_job(dry_run=True)

for hour in range(0, 24, 2):
    schedule.every().day.at('{:02}:01'.format(hour)).do(predict_job)

while True:
    schedule.run_pending()
    time.sleep(1)
