import discord
from discord import utils
from discord.ext import commands
from config import settings

intents = discord.Intents.all()
client = discord.Client(intents=intents)
glib = {}
infoChan = None
infoChanName = "game-list"

#создать role_white_list
#организовать добавление и удаление

#добавить реакции
#написать тестовые события добавления и отмены реакции
#сделать полную версию прошлого пункта

bot = commands.Bot(command_prefix = settings['prefix'])

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel != infoChan or user.id == bot.user.id:
        return
    print(user.name + ' add')

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id != infoChan.id or payload.user_id == bot.user.id:
        return
    user = client.get_user(payload.user_id)
    print(f'{user.name} remove')

@bot.event
async def on_message(mess):
    await bot.process_commands(mess)
    if mess.channel == infoChan and mess.author.id != bot.user.id:
        await mess.delete(delay=1)

@bot.event
async def on_ready():
    bot.command_prefix = f'<@!{bot.user.id}> '
    global infoChan
    guild = bot.guilds[0]

    for ch in guild.channels:
        if ch.name == infoChanName and ch is not None:
            await ch.delete()

    channel = await guild.create_text_channel(infoChanName)
    for role in guild.roles:
        if role.permissions.administrator or role.name == 'Ибо нехуй':
            await channel.set_permissions(role, read_messages=True, send_messages=True, add_reactions = False, manage_messages = False)
        else:
            await channel.set_permissions(role, read_messages=True, send_messages=False, add_reactions = False, manage_messages = False)
    infoChan = channel

    await channel.send('Список игр:')
    glib.update({await channel.send('Список пуст'): ['Список пуст']})
    print(f'LOG_INFO: Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.message.author}!')
    await ctx.message.delete()

@bot.command()
async def addgame(ctx):
    gmesage = list(glib.keys())[0]
    if gmesage.content == 'Список пуст':
        glib.pop(gmesage)
        await gmesage.delete()
    s = ctx.message.content.split(' ')
    s.pop(0)
    s.pop(0)
    s = ' '.join(s)
    for val in glib.values():
        if val[0] == s:
            await ctx.send(f'Игра "{s}" уже в списке!')
            await ctx.message.channel.last_message.delete(delay = 2)
            return
    await ctx.message.delete()
    mess = await infoChan.send(s + ': увы, ¯\_(ツ)_/¯')
    await mess.add_reaction('\U0001F4DD')
    await mess.add_reaction('\U00002795')
    glib.update({mess:[s]})

    print(f'LOG_INFO: addgame {s}')

bot.run(settings['token'])





# with open("team0.pickle", "wb") as f:
#     pickle.dump(team, f)


# with open("team0.pickle", "rb") as f:
#     team = pickle.load(f)