import hashlib
import random
import re
import statistics
import string

import discord
import os
import numpy as np
from Levenshtein import distance as levenshtein_distance

import discorduserids
import sheets
import leaderboards

os.environ['MPLCONFIGDIR'] = os.getcwd() + '/configs/'

f = open('skillissues.txt', 'r', encoding='utf8')
skill_issues = f.readlines()
f.close()
random.shuffle(skill_issues)
issue_index = 0

f = open('pastas.txt', 'r', encoding='utf8')
lines = f.readlines()
f.close()
label_to_pasta = {}
pastas = []
labels = lines[0][1:].strip().split(',')
running = ''
pasta_count = 0
for line in lines[1:]:
    if line[0] == '~':
        for label in labels:
            if label not in label_to_pasta:
                label_to_pasta[label] = []
            label_to_pasta[label].append(pasta_count)
        pastas.append(running)
        running = ''
        pasta_count += 1
        labels = line[1:].strip().split(',')
    else:
        running += line
for label in labels:
    if label not in label_to_pasta:
        label_to_pasta[label] = []
    label_to_pasta[label].append(pasta_count)
pastas.append(running)

curr_str = 'choc can\'t micro rof'
best_str = ('', float('inf'))


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
        if identifier in label_to_pasta:
            return pastas[random.choice(tuple(label_to_pasta[identifier]))]
    return random.choice(pastas)


def matching_pastas(identifier, select=None):
    matching = []
    if not identifier:
        for noodle in pastas:
            noodle = noodle[0: 25].replace('\n', ' ')
            matching.append(f'{noodle} ...')
        return matching
    if identifier not in label_to_pasta:
        return None
    for pasta_index in label_to_pasta[identifier]:
        matching.append(pastas[pasta_index])
    if select:
        return matching[select - 1]
    matching = [f'{pasta[0: 25].replace(chr(10), " ")} ...' for pasta in matching]
    return matching


def random_issue(args):
    if args:
        s = strip_to_words(args)
        hash_val = int(hashlib.sha1(s.encode('utf-8')).hexdigest(), 16)
        return skill_issues[hash_val % len(skill_issues)]
    global issue_index
    if issue_index >= len(skill_issues):
        random.shuffle(skill_issues)
        issue_index = 0
    issue = skill_issues[issue_index]
    issue_index += 1
    return issue


def ranks_embed(stats, *identifiers):
    import matplotlib.pyplot as plot
    num_races = len(sheets.all_ids)
    plot.clf()
    plot.axis([1, num_races, 1, 100])
    plot.grid(color='grey', alpha=0.5)
    num_identifiers = len(identifiers)
    first_identifier, first_ranks, first_bestfit = None, None, None

    cmap = plot.get_cmap('gist_heat')
    colors = [cmap(i / num_identifiers) for i in range(num_identifiers)]
    for index, identifier in enumerate(identifiers):
        user_id = None
        if identifier[0: 2] == '<@' and identifier[-1:] == '>':
            user_id = discorduserids.get_id(identifier[2: -1])
            user_id = sheets.known(user_id)
        if not user_id:
            user_id = sheets.known(identifier)
        all_ranks = leaderboards.get_all_rank(user_id[0])
        if not all_ranks:
            continue
        if user_id[0] == '5b2845abfcd0f8d9745e6cfe':
            all_ranks = [(entry[0], (entry[1] - 1) % 20 + 81) for entry in all_ranks]
        elif user_id[0] == '5b7f82e318c7cbe32fa01e4e':
            all_ranks = [(entry[0], (entry[1] - 1) % 20 + 1) for entry in all_ranks]
        x = [entry[0] for entry in all_ranks]
        y = [entry[1] for entry in all_ranks]
        plot.plot(x, y, '.', color=colors[index], label=user_id[1])
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plot.plot(x, p(x), '--', color=colors[index])

        if index == 0:
            first_identifier = user_id[1]
            first_ranks = all_ranks
            first_bestfit = p
    plot.legend(loc='best')
    plot.savefig('output.png')

    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    file = discord.File('output.png', filename='image.png')
    embed.set_image(url='attachment://image.png')

    if stats:
        best = min(first_ranks, key=lambda entry: entry[1])
        worst = max(first_ranks, key=lambda entry: entry[1])
        embed.set_author(name=f'Stats for {first_identifier} across {len(first_ranks)} tracked races')
        embed.add_field(name='Best tracked performance', value=f'Rank {best[1]} in race {best[0]}', inline=False)
        embed.add_field(name='Worst tracked performance', value=f'Rank {worst[1]} in race {worst[0]}', inline=False)
        embed.add_field(name='Average rank', value=str(round(statistics.median([entry[1] for entry in first_ranks]))),
                        inline=False)
        embed.add_field(name=f'Predicted ranking in race {num_races + 1}', value=str(round(first_bestfit(num_races))),
                        inline=False)

    return file, embed


def validate_str(hello_target):
    r = re.compile(r'.*@[^!\d].*')
    return not r.match(hello_target)


def space_by_caps(name):
    import re
    return re.sub(r'([A-Z])', r' \1', name).strip()


def rofify(img_url):
    import requests
    from PIL import Image
    r = requests.get(img_url)
    with open('temp.png', 'wb') as out_img:
        out_img.write(r.content)
    to_rof = Image.open('temp.png')
    to_rof_w, to_rof_h = to_rof.size
    if to_rof_w > to_rof_h:
        ratio = 144 / to_rof_w
        new_w = max(1, int(ratio * to_rof_h))
        to_rof = to_rof.resize((144, new_w), Image.LANCZOS)
        offset = (144, 216 - int(new_w / 2))
    else:
        ratio = 144 / to_rof_h
        new_h = max(1, int(ratio * to_rof_w))
        to_rof = to_rof.resize((new_h, 144), Image.LANCZOS)
        offset = (216 - int(new_h / 2), 144)
    rof = Image.open('ring.png')
    rof.paste(to_rof, offset, to_rof.convert('RGBA'))
    rof.save('temp.png')


def str_check(test_str):
    global best_str

    dist = levenshtein_distance(test_str, curr_str)
    if test_str != curr_str and test_str in curr_str.split(' '):
        return 'Your response is part of the correct answer'
    if dist == 0:
        return 'Correct, notifying <@!279126808455151628>'
    if test_str in curr_str.split(' '):
        return 'Your response is part of the correct answer'
    if dist < best_str[1]:
        best_str = (test_str, dist)
    return f'You\'re off by {dist}'
