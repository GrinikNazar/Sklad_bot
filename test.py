import time
import engine

def time_mod(tm):
    time_b_list = tm.split(':')
    time_b_list = list(map(lambda x: int(x), time_b_list))
    result = (time_b_list[0] * 60) * 60 + time_b_list[1] * 60
    return result

def sleep_time(start_time, end_time):
    result = end_time - start_time
    if result < 0:
        result = result * -1
    s_tome_sec = (24 * 60) * 60
    result = s_tome_sec - result - 5
    return result

def str_time_t():
    t = time.time()
    t = time.localtime(t)
    t = time.strftime('%H:%M', t)
    return t
    
time_b = '14:30'

t = time.time()

print(t)