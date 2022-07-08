import time
import threading
import random

s = 'rgerger 2'
if s.split(' ')[-1].isdigit():
    number = int(s.split(' ')[-1])
    print(number)
    print(type(number))