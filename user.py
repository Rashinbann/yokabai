import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


@commands.command()
async def user(ctx, *name):
    user = ctx.message.content.removeprefix(".user ")
    page = requests.get(f"https://anilist.co/user/{user}")
    soup = BeautifulSoup(page.text, features="html.parser")
    username = soup.find('h1', attrs={'class': 'name'}).string
    avatar = soup.findAll('img', attrs={'class': 'avatar'})
    link = avatar[0]
    getlink = link.get('src')
    about = soup.find('div', attrs={'class': 'about'}).string
    totalAni = soup.find('div', attrs={'class': 'value'}).string
    embed = discord.Embed(
        title=username
    )
    embed.set_thumbnail(url=getlink)
    embed.set_author(name='Go to page',
                     url=f"https://anilist.co/user/{user}")
    embed.insert_field_at(0, name='About', value=about)
    embed.insert_field_at(1, name='Info', value=totalAni)
    await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(user)
