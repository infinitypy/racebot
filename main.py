from discord.ext import commands
import datetime
import sheets

client = commands.Bot(command_prefix='~')


@client.event
async def on_ready():
    print(f'{client.user} is online')


@client.command()
async def hello(ctx):
    await ctx.send('hello')


@client.command()
async def race(ctx, num):
    await ctx.send(sheets.get_race_name(num))


@client.command()
async def length(ctx, num, abr=None):
    await ctx.send('Round ' + num + ' is ' + sheets.length(int(num), abr) + 's')


@client.command()
async def rtime(ctx, start, end, stime, abr=None):
    longest, longest_round = sheets.last_bloon_time(int(start), int(end), float(stime), abr)
    final_time = str(datetime.timedelta(seconds=longest))[3:-4]
    await ctx.send('You will get **' + final_time + '** if you perfect clean round ' + str(longest_round))


client.run('ODkzMjkxMjI1NTY4OTE5NTYy.YVZUSA.qCUMnKzLJsIu0X_TCEI5BnvST8k')
