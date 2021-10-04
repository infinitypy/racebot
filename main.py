import os
from discord.ext import commands
import datetime
import sheets, leaderboard

#from webserver import keep_alive

client = commands.Bot(command_prefix='~')


@client.event
async def on_ready():
    print(f'{client.user} is online')


@client.command()
async def femdom(ctx):
    await ctx.send('if I may offer input, ezili seems restrained rather than an actual bottom, if you get her to open up then she will absolutely destroy you'
'\ngwen strikes me as the type to act tough on the field but enjoy cuddles and rainbows and stuff')


@client.command()
async def dominaciónfemenina(ctx):
    await ctx.send('si puedo aportar, ezili parece retraida mas que un fondo, si logras que se abra, ella te destruira\ngwen me parece que es el tipo que intenta actuar duro pero en el fondo adora los cariños y arcoiris y esas cosas')


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
            print('bad input')
    except ValueError:
        print('bad input')


@client.command()
async def length(ctx, num, abr=None):
    try:
        if 0 < int(num) <= 140:
            await ctx.send('Round ' + num + ' is ' + sheets.length(int(num), abr) + 's')
        else:
            print('bad input')
    except ValueError:
        print('bad input')


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
        print('bad input')


@client.command()
async def info(ctx, num):
    try:
        if int(num) > 0:
            await ctx.send('\n'.join(sheets.info(int(num))))
    except ValueError:
        print('bad input')

@client.command()
async def lb(ctx, first, last):
    await ctx.send("```" + leaderboard.getleaderboard(int(first), int(last)) + "```")



keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)
