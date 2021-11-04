import datetime
import os
import statistics
import string

import discord
import matplotlib.pyplot as plot
import numpy as np
from discord import HTTPException
from discord.ext import commands

import discorduserids
import leaderboard
import misc
import profiles
import sheets
import timetravel.newracedecode

# from webserver import keep_alive

client = commands.Bot(command_prefix=['r!', 'R!', 'rof🔥', 'ROF🔥'])
client.remove_command('help')


@client.command(pass_context=True)
async def help(ctx, command_name=None):
    command_help = {
        'hello': ['name:opt', 'Says hello'],
        'invite': ['none', 'Returns bot invite'],
        'race': ['race_number [race_end]', 'returns [a range of] race name'],
        'length': ['round_number', 'returns round length'],
        'rtime': ['start_round end round send time', 'returns calculated time'],
        'lb': ['race_number first:opt last:opt', 'returns the lb'],
        'id': ['race_number rank', 'returns the userid'],
        'nicks': ['userid:opt', 'returns all used nicknames'],
        'rank': ['userid:opt', 'returns rank in the current race'],
        'ranks': ['userid:opt', 'returns stats about rankings'],
        'profile': ['userid:opt', 'returns stats'],
        'nkinfo': ['race name', 'returns info for the race'],
        'getid': ['none', 'returns your linked id'],
        'setid': ['userid',
                  'saves a userid to your discord allowing you to leave the userid section for other commands blank'],
        'unlink': ['none', 'unlinks your userid'],
        'pasta': ['label:opt', 'pasta'],
        'diagnosis': ['patient:opt', 'skill issue'],
        'badgelb': ['none', 'returns a badge leaderboard'],
        'newrace': ['none', 'returns the latest race name/id']
    }

    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    if not command_name:
        embed.set_author(name='Help')
        embed.add_field(name='Command list', value=', '.join(list(command_help.keys())), inline=False)
        embed.add_field(name='Help usage', value='help command_name, returns what the command does and how to use it',
                        inline=False)
    elif command_name in command_help:
        embed.set_author(name=f'Help for "{command_name}" command')
        embed.add_field(name='Usage', value=command_help[command_name][0], inline=False)
        embed.add_field(name='Function', value=command_help[command_name][1])
    else:
        embed.set_author(name='Help')
        embed.add_field(name=command_name, value='Not a valid command, use r!help for a list of commands', inline=False)

    embed.set_thumbnail(url=ROF)
    await ctx.send(embed=embed)


ROF = 'https://cdn.discordapp.com/emojis/859285402749632522.png?size=96'
BIG_ERROR = 'Too much text. Please select a smaller range.'


@client.event
async def on_ready():
    print(f'{client.user} is online')


@client.command()
async def hello(ctx, *args):
    if not args:
        await ctx.send('hello')
    else:
        name = ' '.join(args)
        if name == 'exephur':
            await ctx.send('All the homies hate exephur')
        else:
            await ctx.send(f'hello {name}')


@client.command()
async def invite(ctx):
    await ctx.send('https://discord.com/oauth2/authorize?'
                   'client_id=893291225568919562&permissions=3072&scope=bot')


@client.command()
async def race(ctx, num, num_end=None, race_id=None):
    if not race_id:
        if not num_end:
            output = sheets.race(num, None)
        elif num_end.isdigit():
            output = sheets.race_range(num, num_end, None)
        else:
            output = sheets.race(num, num_end)
    else:
        output = sheets.race_range(num, num_end, race_id)
    if not output:
        await ctx.send(ROF)
        return
    try:
        await ctx.send(output)
    except HTTPException:
        await ctx.send(BIG_ERROR)


@client.command()
async def length(ctx, num, abr=None):
    try:
        if 0 < int(num) <= 140:
            await ctx.send(f'Round {num} is {sheets.length(int(num), abr)}s')
        else:
            await ctx.send(ROF)
    except ValueError:
        await ctx.send(ROF)


@client.command()
async def rtime(ctx, start, end, stime=None, abr=None):
    if not stime and not abr:
        stime = 0
    try:
        if 0 <= int(start) <= 140 and 0 < int(end) <= 141 and \
                int(start) < int(end) and float(stime) >= 0:
            longest, longest_round = sheets.rtime(int(start), int(end), float(stime), abr)
            final_time = str(datetime.timedelta(seconds=longest))[3:-4]
            await ctx.send(f'You will get **{final_time}** if you perfect clean round {longest_round}')
        else:
            await ctx.send(ROF)
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
    title = f'Race # {race_num}: **{sheets.race(str(race_num))}**'
    output = leaderboard.get_leaderboard(int(race_num))
    if output:
        output_str = ''
        for i in range(int(last) - int(first) + 1):
            if len(output[0]) == 3:
                output_str += '\n{} {} {}' \
                    .format(str(i + int(first)).ljust(2), output[i + int(first) - 1][2], output[i + int(first) - 1][1])
            else:
                output_str += '\n{} {} {}' \
                    .format(str(i + int(first)).ljust(2), output[i + int(first) - 1][1], output[i + int(first) - 1][0])
    else:
        output_str = 'No data'
    await ctx.send(f'{title}```{output_str}```')


@client.command()
async def id(ctx, race_num=None, user_rank=None):
    if not user_rank and not race_num:
        output = sheets.from_discord_id(str(ctx.message.author.id))
    else:
        if not user_rank:
            user_rank = race_num
            race_num = len(leaderboard.all_ids)
        output = leaderboard.get_id(int(race_num), user_rank)
    if not output:
        await ctx.send(ROF)
        return
    await ctx.send(f'**{output[1]}**\'s user ID:')
    await ctx.send(output[0])


@client.command()
async def nicks(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await ctx.send(ROF)
            return
    user_id = sheets.known(identifier)
    output = leaderboard.get_nicks(user_id[0])
    if not output:
        await ctx.send(ROF)
        return

    nicknames = ''
    for entry in output:
        nicknames += '\n' + f'{entry[1]:>2}: {entry[0]}'

    await ctx.send(f'Nicknames for **{user_id[1]}**```\n{nicknames}```')


@client.command()
async def rank(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await ctx.send(ROF)
            return
    user_id = sheets.known(identifier)
    output = leaderboard.get_rank(len(leaderboard.all_ids), user_id[0])
    if not output:
        await ctx.send(ROF)
        return
    await ctx.send(f'**{user_id[1]}**\'s current rank in race {len(leaderboard.all_ids)}: {output}')


@client.command()
async def ranks(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await ctx.send(ROF)
            return
    user_id = sheets.known(identifier)
    all_ranks = leaderboard.get_all_rank(user_id[0])
    if not all_ranks:
        await ctx.send(ROF)
        return
    x = [entry[0] for entry in all_ranks]
    if user_id[0] == '5b2845abfcd0f8d9745e6cfe':
        all_ranks = [(entry[0], (entry[1] - 1) % 20 + 81) for entry in all_ranks]
    elif user_id[0] == '5b7f82e318c7cbe32fa01e4e':
        all_ranks = [(entry[0], (entry[1] - 1) % 20 + 1) for entry in all_ranks]
    y = [entry[1] for entry in all_ranks]
    num_races = len(leaderboard.all_ids)
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

    embed.set_author(name=f'Stats for {user_id[1]} across {len(all_ranks)} tracked races')
    embed.add_field(name='Best tracked performance', value=f'Rank {best[1]} in race {best[0]}', inline=False)
    embed.add_field(name='Worst tracked performance', value=f'Rank {worst[1]} in race {worst[0]}', inline=False)
    embed.add_field(name='Average rank', value=str(round(statistics.median([entry[1] for entry in all_ranks]))),
                    inline=False)
    embed.add_field(name=f'Predicted ranking in race {num_races + 1}', value=str(round(p(num_races))),
                    inline=False)

    file = discord.File('output.png', filename='image.png')
    embed.set_image(url='attachment://image.png')
    await ctx.send(file=file, embed=embed)
    os.remove('output.png')


@client.command()
async def profile(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await ctx.send(ROF)
            return
    user_id = sheets.known(identifier)
    output = profiles.get_profile(user_id[0])
    if not output:
        await ctx.send(ROF)
        return
    await ctx.send(profiles.get_profile(user_id[0]))


@client.command()
async def newrace(ctx):
    await ctx.send(timetravel.newracedecode.events())


@client.command()
async def nkinfo(ctx, name=None):
    if name == None:
        name = timetravel.newracedecode.events('name')
    await ctx.send(timetravel.newracedecode.raceinfo(name))


@client.command()
async def getid(ctx):
    output = discorduserids.get_id(ctx.message.author.id)
    if not output:
        await ctx.send(ROF)
        return
    await ctx.send('User ID:')
    await ctx.send(output)


@client.command()
async def setid(ctx, u_id=None):
    if not u_id:
        await ctx.send(ROF)
        return
    text = 'Replacement' if discorduserids.set_id(ctx.message.author.id, u_id) else 'New'
    await ctx.send(f'{text} user ID: ``{u_id}``')


@client.command()
async def unlink(ctx):
    removed = discorduserids.remove_id(ctx.message.author.id)
    output = f'**{ctx.message.author.id}** successfully unlinked' if removed else 'Nothing linked'
    await ctx.send(output)


@client.command()
async def pasta(ctx, *args):
    if args:
        identifier = ''.join(args)
        for c in string.punctuation:
            identifier = identifier.replace(c, '')
    else:
        identifier = None
    test = misc.random_pasta(identifier)
    await ctx.send(test)


@client.command()
async def diagnosis(ctx, *args):
    name = ' '.join(args) if args else None
    header = name + '\'s diagnosis: ' if name else 'Diagnosis: '
    await ctx.send(header + misc.random_issue(name))


blb = 'None, run ``r!badgelb update`` to populate'


@client.command()
async def badgelb(ctx, update=None):
    global blb
    if update == 'update':
        await ctx.send('updating (this takes about 30 seconds)')
        blb = profiles.generate_badge_lb()
        await ctx.send('updated')
    else:
        await ctx.send(blb)


# keep_alive()
# my_secret = os.environ['TOKEN']
my_secret = 'ODkzOTY2NjkwNzY4MDA3MTc4.YVjJXA.Az511XCUNfFgEDdciex3s3pHzVw'
client.run(my_secret)
