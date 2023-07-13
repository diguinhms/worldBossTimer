import asyncio
import discord
import os
import requests
from discord.ext import commands
from dotenv import load_dotenv

saved_channel_id = 0

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def set_channel(ctx):
    channel_id = ctx.channel.id
    save_channel_id(channel_id)
    await ctx.send(f'O canal {ctx.channel.mention} foi configurado como o canal de envio de mensagens do bot.')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    while True:
        response = requests.get('https://api.worldstone.io/world-bosses/')
        boss_data = response.json()

        boss_name = boss_data["name"]
        boss_timer = boss_data["time"]

        print(boss_timer)

        if boss_timer == 30:
            channel_id = get_saved_channel_id()
            if channel_id:
                match boss_name:
                    case "Avarice":
                        embedMessage = discord.Embed(
                            title="Avarice, The Gold-cursed",
                            description="@everyone, o boss do mundo  irá spawnar em 30 minutos",
                            colour=discord.Colour.from_rgb(201, 159, 59)
                        )
                        embedMessage.set_image(url="https://www.pcgamesn.com/wp-content/sites/pcgamesn/2023/06/diablo"
                                                   "-4-avarice-the-gold-cursed.jpg")
                    case "Wandering Death":
                        embedMessage = discord.Embed(
                            title="The Wandering Death",
                            description="@everyone, o boss do mundo  irá spawnar em 30 minutos",
                            colour=discord.Colour.from_rgb(63, 255, 190)
                        )
                        embedMessage.set_image(
                            url="https://www.pcgamesn.com/wp-content/sites/pcgamesn/2023/06/diablo-4-wandering-death"
                                "-1-1.jpg")
                    case "Ashava":
                        embedMessage = discord.Embed(
                            title="Ashava, The Pestilent",
                            description="@everyone, o boss do mundo irá spawnar em 30 minutos",
                            colour=discord.Colour.from_rgb(146, 101, 82)
                        )
                        embedMessage.set_image(
                            url="https://phantom-marca.unidadeditorial.es/c52fcd9c940721f6b294d530a2306030/resize/828"
                                "/f/jpg/assets/multimedia/imagenes/2023/05/29/16853787184425.jpg")
                channel = bot.get_channel(channel_id)
                await channel.send(embed=embedMessage)

        await asyncio.sleep(60)


def save_channel_id(channel_id):
    global saved_channel_id
    saved_channel_id = channel_id


def get_saved_channel_id():
    return saved_channel_id


bot.run(os.getenv("TOKEN"))
