import time
import threading
import random
from fuzzywuzzy import fuzz




# l = 'iphone 8Plus'
# l2 = 'iphone 8plus'
# l = 'акб нова'
# l2 = 'ноe ак'

# x = fuzz.ratio(l.lower(), l2.lower())
# y = fuzz.token_sort_ratio(l, l2)

# print(x)
# print(y)

users = {
    'Назар': 1,
    'Ваня': 2,
    'Саша': 3,
    'Артур': 4,
    'Льоша': 5,
    'Вадим': 6
}

value = 1

for k, v in users.items():
    if v == value:
        print(k)