import discord
from discord.ext import commands
import asyncio
from config import GUILD_ID, ROLE_ID, PREDEFINED_CHANNEL_ID, WELCOME_MESSAGE, FIVEM_CONNECT

# Variável global para armazenar a mensagem de boas-vindas configurada
welcome_message = WELCOME_MESSAGE
fivem_connect = FIVEM_CONNECT

class ConnectButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Connect to FiveM", url=f"https://{fivem_connect}"))

async def on_ready(bot):
    print(f'{bot.user} has connected to Discord!')

async def on_member_join(member, bot):
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if guild is None:
        print("Guild not found!")
        return
    
    role = guild.get_role(ROLE_ID)
    if role is None:
        print("Role not found!")
        return
    
    try:
        await member.add_roles(role)
        print(f"Assigned role {role.name} to {member.name}.")
    except Exception as e:
        print(f"Error assigning role: {e}")

    # Enviar mensagem de boas-vindas na DM
    try:
        await member.send(welcome_message)
        print(f"Sent welcome message to {member.name}.")
    except Exception as e:
        print(f"Error sending welcome message: {e}")

async def send_message(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Por favor, forneça o título da mensagem:")

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60)
        message_title = msg.content
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")
        return

    await ctx.send("Por favor, forneça o conteúdo da mensagem:")

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60)
        message_content = msg.content
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")
        return

    channel = ctx.bot.get_channel(PREDEFINED_CHANNEL_ID)
    if channel is None:
        await ctx.send("Canal não encontrado!")
        return
    
    embed = discord.Embed(
        title=message_title,
        description=message_content,
        color=discord.Color.blue()
    )
    
    try:
        await channel.send(embed=embed)
        await ctx.send(f"Mensagem enviada para {channel.mention}")
    except Exception as e:
        await ctx.send(f"Erro ao enviar mensagem: {e}")
        print(f"Erro ao enviar mensagem para o canal {PREDEFINED_CHANNEL_ID}: {e}")

async def social(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Por favor, forneça o ID do canal:")

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60)
        channel_id = int(msg.content)
    except ValueError:
        await ctx.send("ID do canal inválido. Por favor, tente novamente.")
        return
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")
        return

    channel = ctx.bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Canal não encontrado!")
        return

    view = discord.ui.View()

    while True:
        await ctx.send("Por favor, forneça o nome da rede social (ou digite 'fim' para terminar):")

        try:
            msg = await ctx.bot.wait_for('message', check=check, timeout=60)
            social_name = msg.content
            if social_name.lower() == 'fim':
                break
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado. Por favor, tente novamente.")
            return

        await ctx.send("Por favor, forneça o link da rede social:")

        try:
            msg = await ctx.bot.wait_for('message', check=check, timeout=60)
            social_link = msg.content
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado. Por favor, tente novamente.")
            return

        view.add_item(discord.ui.Button(label=social_name, url=social_link))

    embed = discord.Embed(
        title="Siga-nos nas Redes Sociais",
        description="Clique nos botões abaixo para nos seguir nas redes sociais.",
        color=discord.Color.blue()
    )

    try:
        await channel.send(embed=embed, view=view)
        await ctx.send(f"Mensagem enviada para {channel.mention}")
    except Exception as e:
        await ctx.send(f"Erro ao enviar mensagem: {e}")
        print(f"Erro ao enviar mensagem para o canal {channel_id}: {e}")

async def set_welcome_message(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Por favor, forneça a nova mensagem de boas-vindas:")

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60)
        global welcome_message
        welcome_message = msg.content
        await ctx.send(f"Mensagem de boas-vindas atualizada para: {welcome_message}")
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")

async def show_fivem_connect(ctx):
    await ctx.send(f"Acesse a cidade do FiveM usando o seguinte link:\n{fivem_connect}")

async def set_fivem_connect(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Por favor, forneça o novo link de conexão do FiveM:")

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60)
        global fivem_connect
        fivem_connect = msg.content
        await ctx.send(f"Link de conexão do FiveM atualizado para: {fivem_connect}")
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")

async def send_connect_button(ctx):
    embed = discord.Embed(
        title="Conecte-se ao FiveM",
        description="Clique no botão abaixo para conectar-se ao nosso servidor do FiveM.",
        color=discord.Color.blue()
    )
    view = ConnectButton()
    await ctx.send(embed=embed, view=view)

async def clear(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Você tem certeza que deseja limpar todas as mensagens? Responda com 'sim' ou 'não'.")

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=30)
        if msg.content.lower() != 'sim':
            await ctx.send("Comando de limpar mensagens cancelado.")
            return
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Comando de limpar mensagens cancelado.")
        return

    def not_pinned(message):
        return not message.pinned

    await ctx.send("Limpando todas as mensagens...")
    
    deleted = 0
    while True:
        deleted_messages = await ctx.channel.purge(limit=100, check=not_pinned)
        deleted += len(deleted_messages)
        if len(deleted_messages) < 100:
            break

    await ctx.send(f"Todas as mensagens foram apagadas. Total de mensagens apagadas: {deleted}", delete_after=5)
