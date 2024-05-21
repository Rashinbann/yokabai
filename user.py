import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

def pretty_list(l, sep='\n'):
    return sep.join(l)

@commands.command()
async def user(ctx, *name):
    user = ctx.message.content.removeprefix(".user ")
    page = requests.get(f"https://anilist.co/user/{user}")
    soup = BeautifulSoup(page.text, features="html.parser")
    username = soup.find('h1', attrs={'class': 'name'}).string
    avatar = soup.findAll('img', attrs={'class': 'avatar'})[0].get('src')
    about = soup.find('div', attrs={'class': 'about'}, recursive=True).get_text()
    print(about)
    stats = soup.findAll('div', attrs={'class': 'stat'})
    data = [stat.findChildren('div', attrs={'class': 'value'}, recursive=False)[0].string for stat in stats]
    embed = discord.Embed(
        title=username
    )
    embed.set_thumbnail(url=avatar)
    embed.set_author(name='Go to page',
                     url=f"https://anilist.co/user/{user}")
    embed.insert_field_at(0, name='About', value=about)
    gay = [f'Total anime: {data[0]}', f'Days watched: {data[1]}', f'Mean score: {data[2]}']
    embed.insert_field_at(1, name='Info', value=pretty_list(gay))
    await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(user)
