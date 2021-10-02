import discord
from discord.ext import commands

client = commands.Bot(command_prefix='~')

@client.event
async def on_ready():
    print(f'{client.user} is online')


@client.command()
async def hello(ctx):
    await ctx.send('hello')



client.run('ODkzMjkxMjI1NTY4OTE5NTYy.YVZUSA.qCUMnKzLJsIu0X_TCEI5BnvST8k')