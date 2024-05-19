import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


page = requests.get("https://en.wiktionary.org/wiki/compersion")
soup = BeautifulSoup(page.text, "html.parser")


word = soup.findAll('span', attrs={'class':'head-wordlline'})

print(word)