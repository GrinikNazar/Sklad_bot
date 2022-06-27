import engine


def handler_wp(message):
    marker = ''
    d = {
        'Готові': [],
        'Клієнтські': [],
        'Не видані': []
    }

    message = message[message.index('Готові'):]

    for msg in message.split('\n'):  
        if msg in d.keys():
            marker = msg
        elif not msg:
            continue
        else:
            d[marker].append(msg)
    
    return d


# print(handler_wp(engine.maket()))