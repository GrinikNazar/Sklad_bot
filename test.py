import win32clipboard

def gen_list(s, apple):
    ks = s.split(' ')[-1].lower()
    s = s.lower().replace(' ', '')[len(apple):-len(ks)]
    s = s.split('/')
    return list(map(lambda x: apple + x + ks, s))


def five(num, max_num):
    s = max_num - num
    while s % 5 != 0:
        s += 1    

    return s
l = ['Назар', 'wegweg', 'qqq']

for i in l:
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText()
    win32clipboard.CloseClipboard()
