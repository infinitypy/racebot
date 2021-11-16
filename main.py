import datetime
import os

import discord
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import discorduserids
import leaderboard
import misc
import profiles
import sheets
import newracedecode
# from webserver import keep_alive
import writelbtosheet

client = commands.Bot(command_prefix=['r!', 'R!', 'rof🔥', 'ROF🔥'], case_insensitive=True)
client.remove_command('help')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        error = str(error)
        await reply(ctx, f'r!{error[error.find(chr(34)) + 1: error.rfind(chr(34))]}'
                         f' does not exist, use r!help to see a list of valid commands', True)
        return
    raise error


@client.command(pass_context=True)
async def help(ctx, command_name=None) -> None:
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
    await ctx.reply(embed=embed)


ROF = 'https://cdn.discordapp.com/emojis/859285402749632522.png?size=96'
BIG_ERROR = 'Too much text. Please select a smaller range.'


@client.event
async def on_ready() -> None:
    print(f'{client.user} is online')


@client.command()
async def hello(ctx, *args) -> None:
    if not args:
        args = [str(ctx.message.author.id)]
        name = f'<@!{args[0]}>'
    else:
        name: str = ' '.join(args)
        if not misc.validate_str(name):
            await reply(ctx, ROF, True)
            return
    hash_val = misc.string_hash(args)
    if hash_val % 5 == 0:
        await reply(ctx, f'All the homies hate {name}')
    else:
        await reply(ctx, f'hello {name}')


@client.command()
async def invite(ctx) -> None:
    await reply(ctx, 'https://discord.com/oauth2/authorize?'
                     'client_id=893291225568919562&permissions=3072&scope=bot')


@client.command()
async def race(ctx, num, num_end=None, race_id=None) -> None:
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
        await reply(ctx, ROF, True)
        return
    try:
        await reply(ctx, output)
    except HTTPException:
        await reply(ctx, BIG_ERROR)


@client.command()
async def length(ctx, num, abr=None):
    try:
        if 0 < int(num) <= 140:
            await reply(ctx, f'Round {num} is {sheets.length(int(num), abr)}s')
        else:
            await reply(ctx, ROF, True)
    except ValueError:
        await reply(ctx, ROF, True)


@client.command()
async def rtime(ctx, start, end, stime=None, abr=None):
    if not stime and not abr:
        stime = 0
    try:
        if 0 <= int(start) <= 140 and 0 < int(end) <= 141 and \
                int(start) < int(end) and float(stime) >= 0:
            longest, longest_round = sheets.rtime(int(start), int(end), float(stime), abr)
            final_time = str(datetime.timedelta(seconds=longest))[3:-4]
            await reply(ctx, f'You will get **{final_time}** if you perfect clean round {longest_round}')
        else:
            await reply(ctx, ROF, True)
    except ValueError:
        await reply(ctx, ROF, True)


@client.command()
async def info(ctx, num):
    try:
        if int(num) > 0:
            await reply(ctx, '\n'.join(sheets.info(int(num))))
    except ValueError:
        await reply(ctx, ROF, True)


@client.command()
async def lb(ctx, race_num=None, first=None, last=None):
    if race_num and first and not last:
        last = first
        first = race_num
        race_num = len(sheets.all_ids)
    if not race_num:
        race_num = len(sheets.all_ids)
    if not first and not last:
        first = 1
        last = 50
    title = f'Race # {race_num}: **{sheets.race(race_num)}**'
    output = leaderboard.get_leaderboard(race_num)
    if output:
        for entry in output:
            res = sheets.known(entry[0])
            if res[0] == res[1]:
                entry[0] = f' ID: {res[1][0:3]}...'
            else:
                entry[0] = res[1]
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
    await reply(ctx, f'{title}```{output_str}```')


@client.command()
async def id(ctx, race_num=None, user_rank=None):
    if not user_rank and not race_num:
        output = sheets.from_discord_id(ctx.message.author.id)
    else:
        if not user_rank:
            user_rank = race_num
            race_num = len(sheets.all_ids)
        output = leaderboard.get_id(race_num, user_rank)
    if not output:
        await reply(ctx, ROF, True)
        return
    await reply(ctx, f'**{output[1]}**\'s user ID:')
    await ctx.send(output[0])


@client.command()
async def nicks(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, ROF, True)
            return
    user_id = sheets.known(identifier)
    output = leaderboard.get_nicks(user_id[0])
    if not output:
        await reply(ctx, ROF, True)
        return

    nicknames = ''
    for entry in output:
        nicknames += '\n' + f'{entry[1]:>2}: {entry[0]}'

    await reply(ctx, f'Nicknames for **{user_id[1]}**```\n{nicknames}```')


@client.command()
async def rank(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, ROF, True)
            return
    user_id = sheets.known(identifier)
    output = leaderboard.get_rank(len(sheets.all_ids), user_id[0])
    if not output:
        await reply(ctx, ROF, True)
        return
    await reply(ctx, f'**{user_id[1]}**\'s current rank in race {sheets.all_ids}: {output}')


@client.command()
async def ranks(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, ROF, True)
            return
    user_id = sheets.known(identifier)
    all_ranks = leaderboard.get_all_rank(user_id[0])
    if not all_ranks:
        await reply(ctx, ROF, True)
        return
    if user_id[0] == '5b2845abfcd0f8d9745e6cfe':
        all_ranks = [(entry[0], (entry[1] - 1) % 20 + 81) for entry in all_ranks]
    elif user_id[0] == '5b7f82e318c7cbe32fa01e4e':
        all_ranks = [(entry[0], (entry[1] - 1) % 20 + 1) for entry in all_ranks]
    file, embed = misc.ranks_embed(user_id[1], all_ranks)
    await ctx.reply(file=file, embed=embed, mention_author=False)
    os.remove('output.png')


@client.command()
async def profile(ctx, identifier=None):
    if not identifier:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, ROF, True)
            return
    user_id = sheets.known(identifier)
    output = profiles.get_profile(user_id[0])
    if not output:
        await reply(ctx, ROF, True)
        return
    await reply(ctx, f'Race stats for **{user_id[1]}**\n{output}')


@client.command()
async def newrace(ctx):
    race_info = newracedecode.events()
    await reply(ctx, f'**Name:** {race_info[0]}\n**ID:** {race_info[1]}')


@client.command()
async def nkinfo(ctx, name=None):
    if not name:
        name = newracedecode.events()[0]
    await reply(ctx, newracedecode.raceinfo(name))


@client.command()
async def getid(ctx):
    output = discorduserids.get_id(ctx.message.author.id)
    if not output:
        await reply(ctx, ROF, True)
        return
    await reply(ctx, 'User ID:')
    await ctx.send(output)


@client.command()
async def setid(ctx, u_id=None):
    if not u_id:
        await reply(ctx, ROF, True)
        return
    res = discorduserids.set_id(u_id, ctx.message.author.id)
    if res is None:
        await reply(ctx, ROF, True)
        return
    text = 'Replacement' if res else 'New'
    await reply(ctx, f'{text} user ID: {u_id}')


@client.command()
async def unlink(ctx):
    removed = discorduserids.remove_id(ctx.message.author.id)
    await reply(ctx, f'**{ctx.message.author.id}** successfully unlinked' if removed else 'Nothing linked')


@client.command()
async def pasta(ctx, *args):
    await reply(ctx, misc.random_pasta(misc.strip_to_words(args) if args else None))


@client.command()
async def diagnosis(ctx, *args):
    name = ' '.join(args) if args else None
    if not misc.validate_str(name):
        await reply(ctx, ROF, True)
        return
    header = name + '\'s diagnosis: ' if name else 'Diagnosis: '
    await reply(ctx, header + misc.random_issue(args))


blb = 'None, run ``r!badgelb update`` to populate'


@client.command()
async def badgelb(ctx, update=None):
    global blb
    if update == 'update':
        await reply(ctx, 'updating (this takes about 30 seconds)')
        blb = profiles.generate_badge_lb()
        await ctx.send('updated')
    else:
        await reply(ctx, blb, True)


@client.command()
async def loadusers(ctx):
    if ctx.message.author.id != 279126808455151628:
        await reply(ctx, ROF, True)
        return
    writelbtosheet.load_all_users()
    await reply(ctx, 'Done loading users')


@client.command()
async def loadnicks(ctx, start=2):
    if ctx.message.author.id != 279126808455151628:
        await reply(ctx, ROF, True)
        return
    writelbtosheet.load_nicks(start)
    await reply(ctx, 'Done loading nicknames')


@client.event
async def on_message(message):
    string = message.content
    if string.strip().startswith('grats'):
        await message.reply('*congrats')
        return
    await client.process_commands(message)


async def reply(ctx, message, mention=False):
    await ctx.reply(message, mention_author=mention)


# keep_alive()
# my_secret = os.environ['TOKEN']
my_secret = 'ODkzOTY2NjkwNzY4MDA3MTc4.YVjJXA.Az511XCUNfFgEDdciex3s3pHzVw'
client.run(my_secret)
