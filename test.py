def gen_list(s, apple):
    ks = s.split(' ')[-1].lower()
    s = s.lower().replace(' ', '')[len(apple):-len(ks)]
    s = s.split('/')
    return list(map(lambda x: apple + x + ks, s))


def five(num):
    max_num = 30
    s = max_num - num
    

    return s

print(five(21))
# print(gen_list('iPhone 7/8/X black', 'iphone'))