import hashlib
import random
import re
import statistics
import string

import discord
import matplotlib.pyplot as plot
import numpy as np

import sheets
import leaderboard

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
                label_to_pasta[label] = set()
            label_to_pasta[label].add(pasta_count)
        pastas.append(running)
        running = ''
        pasta_count += 1
        labels = line[1:].strip().split(',')
    else:
        running += line
for label in labels:
    if label not in label_to_pasta:
        label_to_pasta[label] = set()
    label_to_pasta[label].add(pasta_count)
pastas.append(running)


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


def ranks_embed(stats, *identifiers):
    num_races = len(sheets.all_ids)
    plot.clf()
    plot.axis([1, num_races, 1, 100])
    plot.grid(color='grey', alpha=0.5)
    num_identifiers = len(identifiers)
    first_identifier, first_ranks, first_bestfit = None, None, None

    cmap = plot.get_cmap('gist_heat')
    colors = [cmap(i / num_identifiers) for i in range(num_identifiers)]
    for index, identifier in enumerate(identifiers):
        user_id = sheets.known(identifier)
        all_ranks = leaderboard.get_all_rank(user_id[0])
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


def validate_str(hello_target: str) -> bool:
    r = re.compile(r'.*@[^!\d].*')
    return not r.match(hello_target)


def space_by_caps(name: str) -> str:
    import re
    return re.sub(r'([A-Z])', r' \1', name).strip()
