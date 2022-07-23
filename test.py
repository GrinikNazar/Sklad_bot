import time
import threading
import random
from fuzzywuzzy import fuzz




l = 'iphone 8Plus'
l2 = 'iphone8plus'
# l = 'акб нова'
# l2 = 'ноe ак'

x = fuzz.ratio(l.lower(), l2.lower())
y = fuzz.token_sort_ratio(l, l2)

print(x)
print(y)