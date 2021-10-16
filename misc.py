import random
import statistics
from fuzzywuzzy import fuzz

skill_issues = open('skillissues.txt', 'r', encoding='utf8').readlines()
random.shuffle(skill_issues)
issue_index = 0

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


def random_issue(name):
    if name:
        ring_of_fire = "ring of fire"
        rof = "rof"
        ring_ratios = [fuzz.ratio(ring_of_fire, name.lower()), fuzz.partial_token_set_ratio(ring_of_fire, name),
                       fuzz.partial_token_sort_ratio(ring_of_fire, name), ]
        rof_ratios = [fuzz.ratio(rof, name.lower()), fuzz.partial_token_set_ratio(rof, name),
                      fuzz.partial_token_sort_ratio(rof, name)]
        if max([statistics.mean(ring_ratios), statistics.mean(rof_ratios)]) >= 80:
            return "second longest intermediate map"
    global issue_index
    if issue_index >= len(skill_issues):
        random.shuffle(skill_issues)
        issue_index = 0
    issue = skill_issues[issue_index]
    issue_index += 1
    return issue


def send_as_txt(message):
    f = open('output.txt', 'w')
    f.write(message)
    f.close()
