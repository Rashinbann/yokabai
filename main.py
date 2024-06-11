import discord
from discord.ext import commands
import sqlite3
from dotenv import dotenv_values
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

activity = discord.Activity(name="yokabai", type=discord.ActivityType.competing)
bot = commands.Bot(command_prefix=".", intents=intents, activity=activity)

db = sqlite3.connect("streakdb.db")
cursor = db.cursor()


@bot.event
async def on_ready():
    print("we have logged in as user {0.user}".format(bot))
    await bot.load_extension("streak")
    await bot.load_extension("anilist")
    await bot.load_extension("user")
    await bot.load_extension("neko/neko.py")


TOKEN = dotenv_values(".env").get("YOKABAI_TOKEN") or ""
bot.run(TOKEN)
