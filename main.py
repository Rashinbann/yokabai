import discord
from discord.ext import commands
from discord.ext import tasks, commands
from discord import Intents, Message
import sqlite3
import requests
from dotenv import dotenv_values
import os

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

db = sqlite3.connect('streakdb.db')
cursor = db.cursor()

@bot.event
async def on_ready():
    print("we have logged in as user {0.user}".format(bot))
    await bot.load_extension(f"streak")
    await bot.load_extension(f"anilist")

TOKEN = dotenv_values(".env").get("YOKABAI_TOKEN") or ""
bot.run(TOKEN)