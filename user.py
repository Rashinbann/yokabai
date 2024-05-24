import discord
from discord.ext import commands
from bs4 import BeautifulSoup as bs
import requests
from util import pretty_list
from contextlib import suppress


@commands.command()
async def user(ctx):
    user = ctx.message.content.removeprefix(".user ")
    with suppress(AttributeError):
        page = requests.get(f"https://anilist.co/user/{user}")
        soup = bs(page.text, features="html.parser")
        username = soup.find('h1', attrs={'class': 'name'}).string
        user = ctx.message.content.removeprefix(".user ")
        page = requests.get(f"https://anilist.co/user/{user}")
        soup = bs(page.text, features="html.parser")
        username = soup.find('h1', attrs={'class': 'name'}).string
        avatar = soup.findAll('img', attrs={'class': 'avatar'})[0].get('src')
        banner = soup.findAll('div', attrs={'class': 'banner'})[
            0].get('style')
        banner = banner.replace(")", "").replace(";", "")
        banner = banner.removeprefix("background-image:url(")
        stats = soup.findAll('div', attrs={'class': 'stat'})
        data = [stat.findChildren('div', attrs={'class': 'value'}, recursive=False)[
            0].string for stat in stats]
        embed = discord.Embed(
            title=username
        )
        embed.set_thumbnail(url=avatar)
        embed.set_author(name='Go to page',
                         url=f"https://anilist.co/user/{user}")
        embed.set_image(url=banner)
        if banner == "null":
            embed.set_image(
                url="https://s4.anilist.co/file/anilistcdn/user/banner/12576-PUA8NCbVJsgK.jpg")
        gay = [f'Total anime: {data[0]}', f'Days watched: {
            data[1]}', f'Mean score: {data[2]}']
        gay2 = [f"Total manga: {data[3]}", f"Chapters Read: {
            data[4]}", f"Mean score: {data[5]}"]
        embed.insert_field_at(1, name='Manga info', value=pretty_list(gay2))
        embed.insert_field_at(0, name='Anime Info', value=pretty_list(gay))
        await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(user)
