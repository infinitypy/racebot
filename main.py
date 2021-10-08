import os

import discord
from discord.ext import commands
import datetime
import sheets, leaderboard, misc, profiles

#from webserver import keep_alive

client = commands.Bot(command_prefix='r!')
NUM_RACES = 146
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
            await ctx.send('You will get **' + final_time +
                           '** if you perfect clean round ' + str(longest_round))
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
    title = 'Race #' + str(race_num) + ': **' + sheets.race(int(race_num)) + '**'
    output = leaderboard.get_leaderboard(int(race_num), int(first), int(last)).strip()
    misc.send_as_txt(ctx, output)
    await ctx.send(title, file=discord.File('output.txt'))
    os.remove('output.txt')


@client.command()
async def id(ctx, race_num=None, user_rank=None):
    if not user_rank:
        if not race_num:
            await ctx.send(ROF)
            return
        user_rank = race_num
        race_num = NUM_RACES
    try:
        user_id, name, _ = leaderboard.get_id(int(race_num), user_rank)
        global LAST_ID
        LAST_ID = user_id
        await ctx.send('**' + name + '**\'s user ID:')
        await ctx.send(user_id)
    except Exception:
        await ctx.send(ROF)


@client.command()
async def nicks(ctx, identifier=None):
    if not identifier:
        global LAST_ID
        identifier = LAST_ID
    user_id = sheets.known(identifier)
    output = leaderboard.get_nicks(user_id[0])
    if not output:
        await ctx.send(ROF)
        return
    nicknames = '\n'.join(list(map(str, output)))
    await ctx.send('Nicknames for **' + str(user_id[1]) + '**```\n' + nicknames + '```')


@client.command()
async def rank(ctx, identifier=None):
    if not identifier:
        global LAST_ID
        identifier = LAST_ID
    user_id = sheets.known(identifier)
    output = leaderboard.get_rank(len(leaderboard.all_ids), user_id[0])
    if not output:
        await ctx.send(ROF)
        return
    await ctx.send('**' + user_id[1] + '**\'s current rank in race ' +
                   str(len(leaderboard.all_ids)) + ': ' + str(output))


@client.command()
async def ranka(ctx, identifier=None):
    if not identifier:
        global LAST_ID
        identifier = LAST_ID
    user_id = sheets.known(identifier)
    number, ranksum = leaderboard.get_average_rank(user_id[0])
    if not number:
        await ctx.send(ROF)
        return
    await ctx.send('**' + user_id[1] + '**\'s average rank in ' + str(number) +
                   ' tracked races: ' + str(round(ranksum / number, 1)))


@client.command()
async def rankw(ctx, user_id=None):
    if not user_id:
        global LAST_ID
        user_id = LAST_ID
    user_id = sheets.known(user_id)
    race_num, user_rank = leaderboard.get_worst_rank(user_id[0])
    if not race_num:
        await ctx.send(ROF)
        return
    await ctx.send('**' + user_id[1] + '**\'s worst tracked performance in race ' +
                   str(race_num) + ' with rank ' + str(user_rank))


@client.command()
async def rankb(ctx, user_id=None):
    if not user_id:
        global LAST_ID
        user_id = LAST_ID
    user_id = sheets.known(user_id)
    race_num, user_rank = leaderboard.get_best_rank(user_id[0])
    if not race_num:
        await ctx.send(ROF)
        return
    await ctx.send('**' + user_id[1] + '**\'s best tracked performance in race ' +
                   str(race_num) + ' with rank ' + str(user_rank))


@client.command()
async def pasta(ctx):
    test = misc.random_pasta()
    await ctx.send(test)


@client.command()
async def profile(ctx, user_id):
    user_id = sheets.known(user_id)
    await ctx.send(profiles.getprofile(user_id[0]))


#keep_alive()
#my_secret = os.environ['TOKEN']
my_secret = 'ODkzOTY2NjkwNzY4MDA3MTc4.YVjJXA.pUDjmTzfKqHfF_al8r_Eontv34E'
client.run(my_secret)
