import discord
from discord.ext import commands
from config import TOKEN
import commands as cmd

intents = discord.Intents.default()
intents.members = True  # Permite eventos relacionados a membros
intents.message_content = True  # Permite acesso ao conteúdo das mensagens

bot = commands.Bot(command_prefix='/', intents=intents)

# Adicione os eventos e comandos ao bot
@bot.event
async def on_ready():
    await cmd.on_ready(bot)

@bot.event
async def on_member_join(member):
    await cmd.on_member_join(member, bot)

@bot.command(name='att')
async def send_message(ctx):
    await cmd.send_message(ctx)

@bot.command(name='social')
async def social(ctx):
    await cmd.social(ctx)

@bot.command(name='setwelcome')
async def set_welcome_message(ctx):
    await cmd.set_welcome_message(ctx)

@bot.command(name='connect')
async def show_fivem_connect(ctx):
    await cmd.show_fivem_connect(ctx)

@bot.command(name='setconnect')
async def set_fivem_connect(ctx):
    await cmd.set_fivem_connect(ctx)

@bot.command(name='connectbutton')
async def send_connect_button(ctx):
    await cmd.send_connect_button(ctx)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    await cmd.clear(ctx)

bot.run(TOKEN)
