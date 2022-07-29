import time
import threading
import random
import os

def dict_sum(*args):
   result_dict = {}
   for dict in args:
      for key, value in dict.items():
         if key in result_dict:
            result_dict[key] += value
         else:
            result_dict[key] = value
   return result_dict

a = {'a': 1, 'b': 2, 'c':3}
b = {'a': 1, 'b': 2, 'c':3, 'd': 5}
c = {'a': 6, 'b': 8}
res = {}
res = c.update(b)
print(c)

# r =dict_sum(a, b, c)
# print(r)