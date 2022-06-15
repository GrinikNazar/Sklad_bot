import time
from schedule import every, repeat, run_pending
import schedule
import engine

@repeat(every(1).minutes)
def test_f():
    print('qwe')

while True:
    run_pending()
    time.sleep(1)