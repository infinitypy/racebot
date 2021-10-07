import os
from discord.ext import commands
import datetime
import sheets, leaderboard, misc

#from webserver import keep_alive

client = commands.Bot(command_prefix='r!')
NUM_RACES = 146
LAST_ID = '5b7f82e318c7cbe32fa01e4e'


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
            await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')
    except ValueError:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')


@client.command()
async def length(ctx, num, abr=None):
    try:
        if 0 < int(num) <= 140:
            await ctx.send('Round ' + num + ' is ' + sheets.length(int(num), abr) + 's')
        else:
            await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')
    except ValueError:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')


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
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')


@client.command()
async def info(ctx, num):
    try:
        if int(num) > 0:
            await ctx.send('\n'.join(sheets.info(int(num))))
    except ValueError:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')


@client.command()
async def lb(ctx, racenum=None, first=None, last=None):
    if racenum and first and not last:
        last = first
        first = racenum
        racenum = NUM_RACES
    if not racenum:
        racenum = NUM_RACES
    if not first and not last:
        first = 1
        last = 50
    title = "Race #" + str(racenum) + ": **" + sheets.race(int(racenum)) + "**"
    await ctx.send(title + "```" + leaderboard.get_leaderboard(int(racenum), int(first), int(last)) + "```")


@client.command()
async def id(ctx, race_num=None, rank=None):
    if not rank:
        if not race_num:
            await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')
            return
        rank = race_num
        race_num = NUM_RACES
    try:
        user_id, name, _ = leaderboard.get_id(int(race_num), rank)
        global LAST_ID
        LAST_ID = user_id
        await ctx.send(name + '\'s user ID: ' + user_id)
    except Exception:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')


@client.command()
async def nicks(ctx, user_id=None):
    user_id = sheets.known(user_id)

    if not user_id:
        global LAST_ID
        user_id = LAST_ID

    output = leaderboard.get_nicks(user_id)
    if not output:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')
        return
    nicknames = '\n'.join(list(map(str, output)))
    await ctx.send('Nicknames for **' + str(user_id) + '**```\n' + nicknames + '```')


@client.command()
async def ranka(ctx, user_id=None):
    user_id = sheets.known(user_id)

    if not user_id:
        global LAST_ID
        user_id = LAST_ID
    number, ranksum = leaderboard.get_average_rank(user_id)
    if not number:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')
        return
    await ctx.send("Average rank in " + str(number) + " tracked races: " + str(round(ranksum / number, 1)))


@client.command()
async def rankw(ctx, user_id=None):
    user_id = sheets.known(user_id)

    if not user_id:
        global LAST_ID
        user_id = LAST_ID
    racenum, rank = leaderboard.get_worst_rank(user_id)
    if not racenum:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')
        return
    await ctx.send("Worst tracked performance in race " + str(racenum) + " with rank " + str(rank))


@client.command()
async def rankb(ctx, user_id=None):
    user_id = sheets.known(user_id)

    if not user_id:
        global LAST_ID
        user_id = LAST_ID
    racenum, rank = leaderboard.get_best_rank(user_id)
    if not racenum:
        await ctx.send('https://cdn.discordapp.com/emojis/859285402749632522.png?size=96')
        return
    await ctx.send("Best tracked performance in race " + str(racenum) + " with rank " + str(rank))


@client.command()
async def pasta(ctx):
    test = misc.random_pasta()
    await ctx.send(test)


#keep_alive()
#my_secret = os.environ['TOKEN']
my_secret = 'ODkzOTY2NjkwNzY4MDA3MTc4.YVjJXA.pUDjmTzfKqHfF_al8r_Eontv34E'
client.run(my_secret)
