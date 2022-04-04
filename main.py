import datetime
import os

import discord
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from gspread.exceptions import APIError

import discorduserids
import leaderboards
import misc
import newracedecode
import profiles
import sheets

# from webserver import keep_alive

client = commands.Bot(command_prefix=['r!', 'R!', 'rof!', 'ROF!', 'rof🔥', 'ROF🔥', '🌽🎉'], case_insensitive=True)
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


@client.command(aliases=['r'])
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


@client.command(aliases=['l'])
async def length(ctx, num, abr=None):
    try:
        if 0 < int(num) <= 140:
            await reply(ctx, f'Round {num} {"ABR " if abr else ""}is **{sheets.length(int(num), abr)}**s')
        else:
            await reply(ctx, get_error('length', 0), True)
    except ValueError:
        await reply(ctx, get_error('length', 0), True)


@client.command(aliases=['rt'])
async def rtime(ctx, start, end, stime=None, abr=None):
    if not stime and not abr:
        stime = 0
    try:
        if 0 <= int(start) <= 140 and 0 < int(end) <= 141 and \
                int(start) < int(end) and float(stime) >= 0:
            longest, longest_round = sheets.rtime(int(start), int(end), float(stime), abr)
            final_time = str(datetime.timedelta(seconds=longest))
            if final_time[-4:] == '0000':
                final_time = final_time[3:-4]
            else:
                final_time = final_time[3:] + '.00'
            await reply(ctx, f'You will get **{final_time}** if you perfect clean round {longest_round}')
        else:
            await reply(ctx, get_error('rtime', 0), True)
    except ValueError:
        await reply(ctx, get_error('rtime', 0), True)


@client.command(aliases=['i'])
async def info(ctx, num):
    try:
        if int(num) > 0:
            await reply(ctx, '\n'.join(sheets.info(int(num))))
    except (ValueError, APIError):
        await reply(ctx, get_error('info', 0), True)


@client.command(aliases=['lb'])
async def leaderboard(ctx, race_num=None, first=None, last=None):
    begin_end = [first, last]
    nbegin_end = []
    if race_num and first and not last:
        last = first
        first = race_num
        begin_end = [first, last]
        race_num = len(sheets.all_ids)
    if not first and not last:
        begin_end = [1, 10]
        nbegin_end = [45, 55]
    if race_num and int(race_num) < 0:
        race_num = int(race_num) % len(sheets.all_ids)
    if not race_num:
        title = f'Newest race: **{newracedecode.events()[0]}**'
    else:
        try:
            title = f'Race #{race_num}: **{sheets.race(race_num)}**'
        except APIError:
            await reply(ctx, get_error('leaderboard', 0), True)
            return
    output = leaderboards.get_leaderboard(race_num, True)
    if output:
        for i, entry in enumerate(output):
            res = sheets.known(entry[0])
            if i == 0 and int(begin_end[0]) == 1 and (not res[1] or res[0] == res[1]):
                entry[0] = 'RandyZ524\'s alt'
            elif not res[1] or res[0] == res[1]:
                entry[0] = f' ID: {res[0][0:3]}...'
            else:
                entry[0] = res[1]
        output_str = ''
        for i in range(int(begin_end[1]) - int(begin_end[0]) + 1):
            curr_index = i + int(begin_end[0]) - 1
            adj = 0 if len(output[0]) == 3 else 1
            if curr_index + 1 != 50:
                output_str += f'\n{curr_index + 1:<3} {output[curr_index][2 - adj]} ' \
                              f'{output[curr_index][1 - adj]}'
            else:
                output_str += f'\n50< {output[curr_index][2 - adj]} ' \
                              f'{output[curr_index][1 - adj]}'
        if nbegin_end:
            output_str += '\n...'
            for i in range(int(nbegin_end[1]) - int(nbegin_end[0]) + 1):
                curr_index = i + int(nbegin_end[0]) - 1
                adj = 0 if len(output[0]) == 3 else 1
                if curr_index + 1 != 50:
                    output_str += f'\n{curr_index + 1:<3} {output[curr_index][2 - adj]} ' \
                                  f'{output[curr_index][1 - adj]}'
                else:
                    output_str += f'\n50< {output[curr_index][2 - adj]} ' \
                                  f'{output[curr_index][1 - adj]}'
    else:
        output_str = 'No data'
    try:
        await reply(ctx, f'{title}```{output_str}```')
    except HTTPException:
        await reply(ctx, get_error('leaderboard', 1), True)


@client.command()
async def id(ctx, race_num=None, user_rank=None):
    if not user_rank and not race_num:
        identifier = discorduserids.get_id(ctx.message.author.id)
        output = sheets.known(identifier)
    else:
        if not user_rank:
            user_rank = race_num
            race_num = len(sheets.all_ids)
        output = leaderboards.get_id(race_num, user_rank)
    if not output:
        await reply(ctx, get_error('id', 0), True)
        return
    if output[0] == output[1]:
        await reply(ctx, 'User ID:')
    else:
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
    output = leaderboards.get_nicks(user_id[0])
    if not output:
        await reply(ctx, get_error('nicks', 1), True)
        return
    nicknames = ''
    for entry in output:
        nicknames += '\n' + f'{entry[1]:>2}: {entry[0]}'
    await reply(ctx, f'Nicknames for **{user_id[1]}**```\n{nicknames}```')


@client.command(aliases=['rk'])
async def rank(ctx, *args):
    if not args:
        identifier = discorduserids.get_id(ctx.message.author.id)
        if not identifier:
            await reply(ctx, NO_ID, True)
            return
    else:
        identifier = ' '.join(args)
    user_id = sheets.known(identifier)
    output = leaderboards.get_rank(None, user_id[0])
    if not output:
        await reply(ctx, ROF, True)
        return
    await reply(ctx, f'**{user_id[1]}**\'s current rank in newest race: {output[0]}\n'
                     f'Current time: {output[1]}')


@client.command(aliases=['rks'])
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


@client.command(aliases=['c'])
async def compare(ctx, *args):
    if len(args) == 0:
        await reply(ctx, get_error('compare', 0), True)
        return
    identifiers = [discorduserids.get_id(ctx.message.author.id) if x == 'self' else x for x in args]
    file, embed = misc.ranks_embed(False, *identifiers)
    await ctx.reply(file=file, embed=embed, mention_author=False)
    os.remove('output.png')


@client.command(aliases=['gp'])
async def gaps(ctx, *args):
    if len(args) != 2:
        await reply(ctx, get_error('gaps', 0), True)
        return
    identifiers = [discorduserids.get_id(ctx.message.author.id) if x == 'self' else x for x in args]
    pair_ranks = []
    user_id_1 = sheets.known(identifiers[0])
    all_ranks_1 = leaderboards.get_all_rank(user_id_1[0])
    if not all_ranks_1:
        await reply(ctx, get_error('gaps', 1), True)
        return
    all_ranks_1 = {x[0]: x[1] for x in all_ranks_1}
    user_id_2 = sheets.known(identifiers[1])
    all_ranks_2 = leaderboards.get_all_rank(user_id_2[0])
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


@client.command(aliases=['p'])
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


@client.command(aliases=['nr'])
async def newrace(ctx):
    race_info = newracedecode.events()
    await reply(ctx, f'**Name:** {race_info[0]}\n**ID:** {race_info[1]}')


@client.command(aliases=['nk'])
async def nkinfo(ctx, name=None):
    if not name:
        name = newracedecode.events()[0]
    update = ctx.message.author.id == 279126808455151628
    output = newracedecode.raceinfo(name, update)
    if not output:
        await reply(ctx, ROF)
        return
    await ctx.send(embed=output, mention_author=False)


@client.command(aliases=['gi'])
async def getid(ctx):
    output = discorduserids.get_id(ctx.message.author.id)
    if not output:
        await reply(ctx, NO_ID, True)
        return
    await reply(ctx, 'User ID:')
    await ctx.send(output)


@client.command(aliases=['si'])
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


@client.command(aliases=['ui'])
async def unlink(ctx):
    removed = discorduserids.remove_id(ctx.message.author.id)
    await reply(ctx, f'**{ctx.message.author.id}** successfully unlinked' if removed else 'Nothing linked')


blb = 'None, run ``r!badgelb update`` to populate'


@client.command(aliases=['blb'])
async def badgelb(ctx, update=None):
    global blb
    if update == 'update':
        await reply(ctx, 'updating (this takes about 30 seconds)')
        blb = profiles.generate_badge_lb()
        await ctx.send('updated')
    else:
        await reply(ctx, blb, blb == 'None, run ``r!badgelb update`` to populate')


@client.command()
async def setlink(ctx, link):
    if ctx.message.author.id != 746205219238707210:
        await reply(ctx, ROF, True)
        return
    newracedecode.set_link(link)
    await reply(ctx, 'minecool is the second longest intermediate map')


@client.command(aliases=['pt'])
async def pasta(ctx, *args):
    await reply(ctx, misc.random_pasta(misc.strip_to_words(args) if args else None))


@client.command(aliases=['d'])
async def diagnosis(ctx, *args):
    name = ' '.join(args) if args else None
    if not misc.validate_str(name):
        await reply(ctx, ROF, True)
        return
    header = name + '\'s diagnosis: ' if name else 'Diagnosis: '
    await reply(ctx, header + misc.random_issue(args))


@client.command(aliases=['ntwica'])
async def ntwic(ctx):
    try:
        await ctx.message.delete()
        await ctx.send('<:ntwica:910284846910308465>')
    except discord.errors.Forbidden:
        await reply(ctx, '<:ntwica:910284846910308465>')


@client.command(aliases=['rf'])
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


@client.command(aliases=['fc'])
async def firecredits(ctx, diff, *users: discord.Member):
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
        fc_roles = [str(2 ** x) for x in range(0, 10)]
        diff = int(diff)
        output = {}
        max_display = -1
        for user in users:
            old_fc = 0
            for role in user.roles:
                if role.name in fc_roles:
                    old_fc += int(role.name)
            new_fc = min(max(old_fc + diff, 1), 1023)
            new_roles = []
            temp = new_fc
            for i in range(9, -1, -1):
                if 2 ** i <= temp:
                    temp -= 2 ** i
                    new_roles.append(i)
            to_remove = []
            for role in user.roles:
                if role.name in fc_roles:
                    old_index = fc_roles.index(role.name)
                    if old_index not in new_roles:
                        to_remove.append(role)
                    else:
                        new_roles.remove(old_index)
            await user.remove_roles(*to_remove)
            to_add = []
            for index in new_roles:
                new_role = discord.utils.get(ctx.message.guild.roles, name=str(2 ** index))
                to_add.append(new_role)
            await user.add_roles(*to_add)
            output[user.display_name] = '{:<2} → {:<2}'.format(old_fc, new_fc)
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


@client.command(aliases=['g'])
async def guess(ctx, *args):
    test_str = ' '.join(args)
    if ctx.message.author.id == 279126808455151628 or \
            (ctx.guild.name == 'BTD6 Index' and ctx.channel.name == 'bot-commands'):
        await reply(ctx, misc.str_check(test_str))


@client.command(aliases=['bg'])
async def bestguess(ctx):
    await reply(ctx, f'Current best guess with distance {misc.best_str[1]}:\n'
                     f'```{misc.best_str[0]} ```')


@client.command(aliases=['racism'])
async def racist(ctx):
    await ctx.reply(file=discord.File('racist.png'), mention_author=False)


async def reply(ctx, message, mention=False):
    await ctx.reply(message, mention_author=mention)


def get_error(command_name, error_num):
    return error_messages[command_name][error_num]


# keep_alive()
# my_secret = os.environ['TOKEN']
my_secret = 'ODkzOTY2NjkwNzY4MDA3MTc4.YVjJXA.Az511XCUNfFgEDdciex3s3pHzVw'
client.run(my_secret)
