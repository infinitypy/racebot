import hashlib
import random
import re
import statistics
import string

import discord
import matplotlib.pyplot as plot
import numpy as np

import sheets

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
running = ''
for line in lines[1:]:
    if line[0] == '~':
        pastas[identifiers] = running.strip()
        running = ''
        identifiers = line[1:].strip()
    else:
        running += line
pastas[identifiers] = running.strip()
ids_list = list(pastas.keys())
random.shuffle(ids_list)
pasta_index = 0


def strip_to_words(args):
    s = ''.join(args).lower()
    for c in string.punctuation:
        s = s.replace(c, '')
    return ' '.join(s.split())


def string_hash(args):
    s = strip_to_words(args)
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16)


def random_pasta(identifier=None):
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


def random_issue(args):
    if args:
        s = strip_to_words(args)
        hash_val = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16)
        return skill_issues[hash_val % len(skill_issues)]
    global issue_index
    if issue_index >= len(skill_issues):
        random.shuffle(skill_issues)
        issue_index = 0
    issue = skill_issues[issue_index]
    issue_index += 1
    return issue


def ranks_embed(identifier, all_ranks):
    x = [entry[0] for entry in all_ranks]
    y = [entry[1] for entry in all_ranks]

    num_races = len(sheets.all_ids)
    plot.clf()
    plot.axis([1, num_races, 1, 100])
    plot.grid(color='grey', alpha=0.5)
    plot.plot(x, y, 'k.')

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plot.plot(x, p(x), 'r--')
    plot.savefig('output.png')

    best = min(all_ranks, key=lambda entry: entry[1])
    worst = max(all_ranks, key=lambda entry: entry[1])

    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    embed.set_author(name=f'Stats for {identifier} across {len(all_ranks)} tracked races')
    embed.add_field(name='Best tracked performance', value=f'Rank {best[1]} in race {best[0]}', inline=False)
    embed.add_field(name='Worst tracked performance', value=f'Rank {worst[1]} in race {worst[0]}', inline=False)
    embed.add_field(name='Average rank', value=str(round(statistics.median([entry[1] for entry in all_ranks]))),
                    inline=False)
    embed.add_field(name=f'Predicted ranking in race {num_races + 1}', value=str(round(p(num_races))),
                    inline=False)

    file = discord.File('output.png', filename='image.png')
    embed.set_image(url='attachment://image.png')
    return file, embed


def validate_str(hello_target: str) -> bool:
    r = re.compile(r'.*@[^!\d].*')
    return not r.match(hello_target)
