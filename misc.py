import random
import statistics
from fuzzywuzzy import fuzz

f = open('skillissues.txt', 'r', encoding='utf8')
skill_issues = f.readlines()
f.close()
random.shuffle(skill_issues)
issue_index = 0

f = open('pastas.txt', 'r', encoding='utf8')
lines = f.readlines()
f.close()
pastas = {}
identifiers = lines[0][1:].strip()
running = ""
for line in lines[1:]:
    if line[0] == '~':
        pastas[identifiers] = running.strip()
        running = ""
        identifiers = line[1:].strip()
    else:
        running += line
pastas[identifiers] = running.strip()
ids_list = list(pastas.keys())
random.shuffle(ids_list)
pasta_index = 0


def random_pasta(identifier):
    if identifier:
        for ids in ids_list:
            if identifier in ids.split(','):
                return pastas[ids]
    global pasta_index
    if pasta_index >= len(ids_list):
        random.shuffle(ids_list)
        pasta_index = 0
    pasta = pastas[ids_list[pasta_index]]
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
