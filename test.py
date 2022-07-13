import time
import threading
import random

wp = ['iphone 6 Скло', 'iphone x АКБ', 'iphone 7 Клей АКБ + проклейки', 'iphone 7 Скло', 'iphone 8 Скло']


print(sorted(wp, key=lambda glass: 'Скло' not in glass))