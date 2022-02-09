import datetime
import os

import discord
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from gspread.exceptions import APIError

import discorduserids
import leaderboard
import misc
import newracedecode
import profiles
import sheets

# from webserver import keep_alive

client = commands.Bot(command_prefix=['r!', 'R!', 'rof🔥', 'ROF🔥', '🌽🎉'], case_insensitive=True)
client.remove_command('help')

command_help = {}
f = open('commandhelp.txt', 'r', encoding='utf8')
while command := f.readline():
    command_help[command.strip()] = [f.readline().strip(), f.readline().strip()]

error_messages = {'macros': {}}
f = open('errors.txt', 'r', encoding='utf8')
while macro := f.readline().strip():
    macro = macro.split(':')
    error_messages['macros'][macro[0].strip()] = macro[1].strip()
while command := f.readline().strip():
    error_messages[command] = []
    while error := f.readline().strip():
        if error in error_messages['macros']:
            error = error_messages['macros'][error]
        error_messages[command].append(error)


@client.event
async def on_command_error(ctx, err):
    import difflib
    if isinstance(err, CommandNotFound):
        err = str(err)
        err = err[err.find(chr(34)) + 1: err.rfind(chr(34))]
        matches = difflib.get_close_matches(err, command_help.keys(), n=2)
        if not matches:
            await reply(ctx, f'r!{err} does not exist, use r!help to see a list of valid commands', True)
            return
        matches_str = ' or '.join([f'r!{match}' for match in matches])
        await reply(ctx, f'Did you mean {matches_str}?', True)
        return
    if isinstance(err, MissingRequiredArgument):
        await reply(ctx, error_messages['macros']['MISSING'])
        return
    raise err


@client.command(pass_context=True)
async def help(ctx, command_name=None):
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    if not command_name:
        embed.set_author(name='Help')
        embed.add_field(name='Command list', value=', '.join(list(command_help.keys())), inline=False)
        embed.add_field(name='Help usage', value='r!help command_name, returns what the command does and how to use it',
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
NO_ID = 'No associated ID. Set using r!setid <BTD6 ID>'


@client.event
async def on_ready() -> None:
    print(f'{client.user} is online')


@client.command()
async def hello(ctx, *args) -> None:
    if not args:
        args = [str(ctx.message.author.id)]
        name = f'<@!{args[0]}>'
    else:
        name = ' '.join(args)
        if not misc.validate_str(name):
            await reply(ctx, get_error('hello', 0), True)
            return
    hash_val = misc.string_hash(args)
    if hash_val % 5 == 0:
        await reply(ctx, f'All the homies hate {name}')
    else:
        await reply(ctx, f'hello {name}')


@client.command()
async def hеllo(ctx, *args):
    if ctx.message.author.id != 279126808455151628:
        await hello(ctx, args)
    name = ' '.join(args)
    await reply(ctx, f'All the homies hate {name}')


@client.command()
async def hellо(ctx, *args):
    if ctx.message.author.id != 279126808455151628:
        await hello(ctx, args)
    name = ' '.join(args)
    await reply(ctx, f'hello {name}')


@client.command()
async def invite(ctx) -> None:
    await reply(ctx, 'https://discord.com/oauth2/authorize?'
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
        await reply(ctx, get_error('race', 0), True)
        return
    try:
        await reply(ctx, output)
    except HTTPException:
        await reply(ctx, get_error('race', 1), True)


@client.command()
async def length(ctx, num, abr=None):
    try:
        if 0 < int(num) <= 140:
            await reply(ctx, f'Round {num} {"ABR " if abr else ""}is **{sheets.length(int(num), abr)}**s')
        else:
            await reply(ctx, get_error('length', 0), True)
    except ValueError:
        await reply(ctx, get_error('length', 0), True)


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
            await reply(ctx, get_error('rtime', 0), True)
    except ValueError:
        await reply(ctx, get_error('rtime', 0), True)


@client.command()
async def info(ctx, num):
    try:
        if int(num) > 0:
            await reply(ctx, '\n'.join(sheets.info(int(num))))
    except (ValueError, APIError):
        await reply(ctx, get_error('info', 0), True)


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
    try:
        title = f'Race #{race_num}: **{sheets.race(race_num)}**'
    except APIError:
        await reply(ctx, get_error('lb', 0), True)
        return
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
        await reply(ctx, get_error('id', 0), True)
        return
    await reply(ctx, f'**{output[1]}**\'s user ID:')
    await ctx.send(output[0])


@client.command()
async def nicks(ctx, *args):
    if not args:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, get_error('nicks', 0), True)
            return
    else:
        identifier = ' '.join(args)
    user_id = sheets.known(identifier)
    output = leaderboard.get_nicks(user_id[0])
    if not output:
        await reply(ctx, get_error('nicks', 1), True)
        return
    nicknames = ''
    for entry in output:
        nicknames += '\n' + f'{entry[1]:>2}: {entry[0]}'
    await reply(ctx, f'Nicknames for **{user_id[1]}**```\n{nicknames}```')


@client.command()
async def rank(ctx, *args):
    if not args:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, NO_ID, True)
            return
    else:
        identifier = ' '.join(args)
    user_id = sheets.known(identifier)
    output = leaderboard.get_rank(len(sheets.all_ids), user_id[0])
    if not output:
        await reply(ctx, ROF, True)
        return
    await reply(ctx, f'**{user_id[1]}**\'s current rank in race {len(sheets.all_ids)}: {output}')


@client.command()
async def ranks(ctx, *args):
    if not args:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, NO_ID, True)
            return
    else:
        identifier = ' '.join(args)
    file, embed = misc.ranks_embed(True, identifier)
    await ctx.reply(file=file, embed=embed, mention_author=False)
    os.remove('output.png')


@client.command()
async def compare(ctx, *args):
    if len(args) == 0:
        await reply(ctx, get_error('compare', 0), True)
        return
    identifiers = [discorduserids.get_id(ctx.message.author.id) if x == 'self' else x for x in args]
    file, embed = misc.ranks_embed(False, *identifiers)
    await ctx.reply(file=file, embed=embed, mention_author=False)
    os.remove('output.png')


@client.command()
async def gaps(ctx, *args):
    if len(args) != 2:
        await reply(ctx, get_error('gaps', 0), True)
        return
    identifiers = [discorduserids.get_id(ctx.message.author.id) if x == 'self' else x for x in args]
    pair_ranks = []
    user_id_1 = sheets.known(identifiers[0])
    all_ranks_1 = leaderboard.get_all_rank(user_id_1[0])
    if not all_ranks_1:
        await reply(ctx, get_error('gaps', 1), True)
        return
    all_ranks_1 = {x[0]: x[1] for x in all_ranks_1}
    user_id_2 = sheets.known(identifiers[1])
    all_ranks_2 = leaderboard.get_all_rank(user_id_2[0])
    if not all_ranks_2:
        await reply(ctx, get_error('gaps', 1), True)
        return
    all_ranks_2 = {x[0]: x[1] for x in all_ranks_2}
    for race_rank in all_ranks_2:
        if race_rank in all_ranks_1:
            pair_ranks.append((race_rank, all_ranks_1[race_rank] - all_ranks_2[race_rank]))
    one_best = min(pair_ranks, key=lambda x: x[1])
    two_best = max(pair_ranks, key=lambda x: x[1])
    output = f'Race #{one_best[0]}: {user_id_1[1]} ranked {all_ranks_1[one_best[0]]}, ' \
             f'{user_id_2[1]} ranked {all_ranks_2[one_best[0]]}\n'
    output += f'Race #{two_best[0]}: {user_id_2[1]} ranked {all_ranks_2[two_best[0]]}, ' \
              f'{user_id_1[1]} ranked {all_ranks_1[two_best[0]]}\n'
    await reply(ctx, output)


@client.command()
async def profile(ctx, *args):
    if not args:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, NO_ID, True)
            return
    else:
        identifier = ' '.join(args)
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
async def nkinfo(ctx, name=None, update=None):
    if not name:
        name = newracedecode.events()[0]
    if ctx.message.author.id != 279126808455151628:
        update = None
    output = newracedecode.raceinfo(name, update)
    if not output:
        await reply(ctx, ROF)
        return
    await ctx.send(embed=output, mention_author=False)


@client.command()
async def getid(ctx):
    output = discorduserids.get_id(ctx.message.author.id)
    if not output:
        await reply(ctx, NO_ID, True)
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
async def setlink(ctx, link):
    if ctx.message.author.id != 746205219238707210:
        await reply(ctx, ROF, True)
        return
    newracedecode.set_link(link)


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


@client.command()
async def ntwic(ctx):
    try:
        await ctx.message.delete()
        await ctx.send('<:ntwica:910284846910308465>')
    except discord.errors.Forbidden:
        await reply(ctx, '<:ntwica:910284846910308465>')


@client.command()
async def rofify(ctx, img_link=None):
    import re
    if not img_link:
        try:
            img_link = ctx.message.attachments[0].url
        except IndexError:
            try:
                replied = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                img_link = replied.attachments[0].url
            except Exception:
                img_link = ctx.author.avatar_url
    elif img_link[:2] == '<:':
        img_link = client.get_emoji(int(img_link.split(":")[-1][:-1])).url
    else:
        try:
            user_id = int(re.sub('[^0-9]', '', img_link))
            user = client.get_user(user_id)
            if not user:
                user = await client.fetch_user(user_id)
            img_link = user.avatar_url
        except HTTPException:
            pass
    misc.rofify(img_link)
    await ctx.reply(file=discord.File('temp.png'), mention_author=False)
    os.remove('temp.png')


@client.command()
async def fc(ctx, diff, *users: discord.Member):
    server_name = ctx.guild.name
    if (server_name == 'BTD6 Index' or server_name == 'test') and ctx.message.author.id == 279126808455151628:
        reply_fc = False
        replied = None
        if not users:
            replied = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ctx.guild.get_member(replied.author.id)
            if not user:
                user = await ctx.guild.fetch_member(replied.author.id)
            users = [user]
            reply_fc = True
        fc_roles = [str(x) for x in range(1, 11)]
        fc_roles[0] += ' - overdrive'
        fc_roles[9] += ' - rof'
        diff = int(diff)
        output = {}
        max_display = -1
        for user in users:
            for role in user.roles:
                if role.name in fc_roles:
                    old_index = fc_roles.index(role.name)
                    new_index = min(max(old_index + diff, 0), 9)
                    new_role = discord.utils.get(ctx.message.guild.roles, name=fc_roles[new_index])
                    await user.remove_roles(role)
                    await user.add_roles(new_role)
                    output[user.display_name] = '{:<2} → {:<2}'.format(old_index + 1, new_index + 1)
                    if len(user.display_name) > max_display:
                        max_display = len(user.display_name)
        output_str = '```'
        output_str += '\n'.join(map(lambda x: '{name:>{width}}\'s firecredit score: {res}'
                                    .format(name=x, width=max_display, res=output[x]), output))
        output_str += '```'
        if not reply_fc:
            await reply(ctx, output_str)
        else:
            await ctx.message.delete()
            await ctx.send(output_str, reference=replied, mention_author=False)


@client.command()
async def guess(ctx, *args):
    test_str = ' '.join(args)
    if ctx.message.author.id == 279126808455151628 or \
            (ctx.guild.name == 'BTD6 Index' and ctx.channel.name == 'bot-commands'):
        await reply(ctx, misc.str_check(test_str))


async def reply(ctx, message, mention=False):
    await ctx.reply(message, mention_author=mention)


def get_error(command_name, error_num):
    return error_messages[command_name][error_num]


# keep_alive()
# my_secret = os.environ['TOKEN']
my_secret = 'ODkzOTY2NjkwNzY4MDA3MTc4.YVjJXA.Az511XCUNfFgEDdciex3s3pHzVw'
client.run(my_secret)
