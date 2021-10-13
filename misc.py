import random

lines = open('pastas.txt', 'r', encoding='utf8').readlines()
pastas = []
running = ""
for line in lines:
    if line == '~\n':
        pastas.append(running.strip())
        running = ""
    else:
        running += line
pastas.append(running.strip())
random.shuffle(pastas)
pasta_index = 0


def random_pasta():
    global pasta_index
    if pasta_index >= len(pastas):
        random.shuffle(pastas)
        pasta_index = 0
    pasta = pastas[pasta_index]
    pasta_index += 1
    return pasta


def send_as_txt(message):
    f = open('output.txt', 'w')
    f.write(message)
    f.close()
