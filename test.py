import time

def main_time(time_b):

    def time_mod(tm):
        time_b_list = tm.split(':')
        time_b_list = list(map(lambda x: int(x), time_b_list))
        result = (time_b_list[0] * 60) * 60 + time_b_list[1] * 60 + time_b_list[2]
        return result

    def sleep_time(start_time, end_time):
        result = end_time - start_time
        if result < 0:
            result = result * -1
            s_tome_min = (24 * 60) * 60
            result = s_tome_min - result
        return result

    def str_time_t():
        t = time.time()
        t = time.localtime(t)
        t = time.strftime('%H:%M:%S', t)
        return t

    t = str_time_t()

    while True:
        time_sleep = sleep_time(time_mod(t), time_mod(time_b))
        time.sleep(time_sleep)
        print('Ура')
        time.sleep(1)
        t = str_time_t()


main_time('08:10:00')