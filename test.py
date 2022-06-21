import time
import threading
import random

expect = [
    '🇺🇦 Слава Україні 🇺🇦',
    'Ой у лузі червона калина...',
    'рускій корабль іді нахуй',
    '..тін хуйло',
    '2-3 секунди і готово',
    'Так тримати, молодець \U0001F60E',
    'Хочу додому😭',
    'Працюю, на відміну від декого...',
    'Їбашу',
    'Зараз блять...'
]

def test_mod(data, expect):
    i = 0
    while True:
        i += 1
        print(f'{i} : [{threading.currentThread().name}] - {data}')
        print(f'{random.choice(expect)}')
        time.sleep(5)


# time_bud = '07:40:00'


# thr = threading.Thread(target=main_time, args=(time_bud,), name='thr-1')
# thr.start()

test_mod(str(time.time()), expect)