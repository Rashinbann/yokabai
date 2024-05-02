import discord
from discord.ext import commands
from discord.ext import tasks, commands
from discord import Intents, Message
import sqlite3
import requests
import os

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

db = sqlite3.connect('streakdb.db')
cursor = db.cursor()

@bot.command()
async def jisatsushite(ctx):
    await ctx.send("死ねよ")

@tasks.loop(seconds=7200)
async def auto_send(channel : 973174020767907880):
    await channel.send("<@898175728611389451> taci din gura")

@bot.event
async def on_ready():
    print("we have logged in as user {0.user}".format(bot))
    await bot.load_extension(f"streak")
    await bot.load_extension(f"anilist")
    if not auto_send.is_running():
        channel = await bot.fetch_channel(973174020767907880)
        # auto_send.start(channel)

bot.run('MTExMjcxNzgxNDI5NDM4ODc3OQ.G0BEXs.nMtV0pAOw6ZUlbaGnb_FqQKBP9P7ZiQY8LY9EE')