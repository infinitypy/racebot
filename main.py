import datetime
import os
import statistics

import discord
import matplotlib.pyplot as plot
import numpy as np
from discord.ext import commands

import leaderboard
import misc
import profiles
import sheets
import timetravel.newracedecode

# from webserver import keep_alive

client = commands.Bot(command_prefix=['r!', 'R!'])
LAST_ID = '5b7f82e318c7cbe32fa01e4e'
ROF = 'https://cdn.discordapp.com/emojis/859285402749632522.png?size=96'


@client.event
async def on_ready():
    print(f'{client.user} is online')


@client.command()
async def hello(ctx):
    await ctx.send('hello')


@client.command()
async def invite(ctx):
    await ctx.send('https://discord.com/oauth2/authorize?'
                   'client_id=893291225568919562&permissions=3072&scope=bot')


@client.command()
async def race(ctx, num, race_id=None):
    try:
        if int(num) > 0:
            await ctx.send(sheets.race(int(num), race_id))
        else:
            await ctx.send(ROF)
    except ValueError:
        await ctx.send(ROF)


@client.command()
async def length(ctx, num, abr=None):
    try:
        if 0 < int(num) <= 140:
            await ctx.send('Round ' + num + ' is ' + sheets.length(int(num), abr) + 's')
        else:
            await ctx.send(ROF)
    except ValueError:
        await ctx.send(ROF)


@client.command()
async def rtime(ctx, start, end, stime, abr=None):
    try:
        if 0 <= int(start) <= 140 and 0 < int(end) <= 141 and \
                int(start) < int(end) and float(stime) >= 0:
            longest, longest_round = sheets.rtime(int(start), int(end), float(stime), abr)
            final_time = str(datetime.timedelta(seconds=longest))[3:-4]
            await ctx.send('You will get **{}** if you perfect clean round {}'
                           .format(final_time, longest_round))
        else:
            print('bad input')
    except ValueError:
        await ctx.send(ROF)


@client.command()
async def info(ctx, num):
    try:
        if int(num) > 0:
            await ctx.send('\n'.join(sheets.info(int(num))))
    except ValueError:
        await ctx.send(ROF)


@client.command()
async def lb(ctx, race_num=None, first=None, last=None):
    if race_num and first and not last:
        last = first
        first = race_num
        race_num = len(leaderboard.all_ids)
    if not race_num:
        race_num = len(leaderboard.all_ids)
    if not first and not last:
        first = 1
        last = 50
    title = 'Race # {}: **{}**'.format(race_num, sheets.race(int(race_num)))
    output = leaderboard.get_leaderboard(int(race_num))
    if output:
        output_str = ''
        for i in range(int(last) - int(first) + 1):
            output_str += '\n{} {} {}'\
                .format(str(i + int(first)).ljust(2), output[i + int(first) - 1][2], output[i + int(first) - 1][1])
    else:
        output_str = 'No data'
    await ctx.send('{}```{}```'
                   .format(title, output_str))


@client.command()
async def id(ctx, race_num=None, user_rank=None):
    if not user_rank and not race_num:
        output = sheets.from_discord_id(str(ctx.message.author.id))
        print(output)
    else:
        if not user_rank:
            user_rank = race_num
            race_num = len(leaderboard.all_ids)
        output = leaderboard.get_id(int(race_num), user_rank)
    if not output:
        await ctx.send(ROF)
        return
    await ctx.send('**{}**\'s user ID:'
                   .format(output[1]))
    await ctx.send(output[0])


@client.command()
async def nicks(ctx, identifier=None):
    user_id = sheets.known(identifier) if identifier else sheets.from_discord_id(str(ctx.message.author.id))
    output = leaderboard.get_nicks(user_id[0])
    if not output:
        await ctx.send(ROF)
        return
    nicknames = '\n'.join(list(map(str, output)))
    await ctx.send('Nicknames for **{}**```\n{}```'
                   .format(user_id[1], nicknames))


@client.command()
async def rank(ctx, identifier=None):
    user_id = sheets.known(identifier) if identifier else sheets.from_discord_id(str(ctx.message.author.id))
    output = leaderboard.get_rank(len(leaderboard.all_ids), user_id[0])
    if not output:
        await ctx.send(ROF)
        return
    await ctx.send('**{}**\'s current rank in race {}: {}'
                   .format(user_id[1], len(leaderboard.all_ids), output))


@client.command()
async def ranka(ctx, identifier=None):
    user_id = sheets.known(identifier) if identifier else sheets.from_discord_id(str(ctx.message.author.id))
    ranks = leaderboard.get_all_rank(user_id[0])
    if not ranks:
        await ctx.send(ROF)
        return
    x = [entry[0] for entry in ranks]
    if user_id[0] == '5b2845abfcd0f8d9745e6cfe':
        ranks = [(entry[0], 100) for entry in ranks]
    y = [entry[1] for entry in ranks]
    num_races = len(leaderboard.all_ids)
    plot.clf()
    plot.axis([1, num_races, 1, 100])
    plot.grid(color='grey', alpha=0.5)
    plot.plot(x, y, 'k.')

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plot.plot(x, p(x), 'r--')
    plot.savefig('output.png')
    await ctx.send('**{}**\'s average rank in {} tracked races: {}\nPredicted ranking in race 148: {}'
                   .format(user_id[1], len(ranks), round(statistics.median([entry[1] for entry in ranks])),
                           round(p(num_races))),
                   file=discord.File('output.png'))
    os.remove('output.png')


@client.command()
async def rankw(ctx, identifier=None):
    user_id = sheets.known(identifier) if identifier else sheets.from_discord_id(str(ctx.message.author.id))
    race_num, user_rank = leaderboard.get_worst_rank(user_id[0])
    if not race_num:
        await ctx.send(ROF)
        return
    await ctx.send('**{}**\'s worst tracked performance in race {} with rank {}'
                   .format(user_id[1], race_num, user_rank))


@client.command()
async def rankb(ctx, identifier=None):
    user_id = sheets.known(identifier) if identifier else sheets.from_discord_id(str(ctx.message.author.id))
    race_num, user_rank = leaderboard.get_best_rank(user_id[0])
    if not race_num:
        await ctx.send(ROF)
        return
    await ctx.send('**{}**\'s best tracked performance in race {} with rank {}'
                   .format(user_id[1], race_num, user_rank))


@client.command()
async def pasta(ctx):
    test = misc.random_pasta()
    await ctx.send(test)


@client.command()
async def diagnosis(ctx, *args):
    name = ' '.join(args) if args else None
    header = name + '\'s diagnosis: ' if name else 'Diagnosis: '
    await ctx.send(header + misc.random_issue(name))


@client.command()
async def profile(ctx, user_id):
    user_id = sheets.known(user_id)
    await ctx.send(profiles.get_profile(user_id[0]))


@client.command()
async def nkinfo(ctx, name):
    await ctx.send(timetravel.newracedecode.raceinfo(name))


# keep_alive()
# my_secret = os.environ['TOKEN']
my_secret = 'ODkzOTY2NjkwNzY4MDA3MTc4.YVjJXA.pUDjmTzfKqHfF_al8r_Eontv34E'
client.run(my_secret)
