import time
import threading
import random

man = [
    'Вася',
    'Петя'
]

def mod_com(func):
    def wrapper(num, name):
        if name in man:
            print('Додаю')
            result = func(num, name)
        else:
            result = 'oops...'
        return result
    return wrapper

def one_dec(func):
    def wrapper(*args):
        print('Пробний декоратор')
        result = func(*args)
        return result
    return wrapper

@mod_com
@one_dec
def test_mod(num, name):
    num = str(num) * 2
    return num

print(test_mod(1, 'Петя'))