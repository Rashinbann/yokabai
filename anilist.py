import requests
import discord
from discord.ext import commands
from AnilistPython import Anilist
import textwrap
import re

anilist = Anilist()

def ellipcise(text):
    return textwrap.shorten(descdict, width=1024, placeholder="...")


markdown_map = [{tags: ['<i>', '</i>'], markdown: '*'}]
def convert_to_markdown(text, replace_map):
    for replacement in replace_map:
        #? https://stackoverflow.com/questions/70949308/how-to-access-the-matched-value-in-the-default-case-of-structural-pattern-matchi
        match type(replacement):
            case list:
                for tag in replacement['tags']:
                    text.replace(tag, replacement['markdown'])
            case str:
                text.replace(replacement['tag'], replacement['markdown'])
            case _ as bad_type:
                raise TypeError("tags must be of type 'list' or 'str', was {bad_type}")
    return text

def markdownify(text):
    return convert_to_markdown(text, markdown_map)

@commands.command()
async def fox(ctx):
    responsefox = requests.get("https://randomfox.ca/floof")
    fox = responsefox.json()
    await ctx.send(fox['image'])

@commands.command(
    brief="Search Anilist for a manga and post it's info in the chat"
)
async def manga(ctx, *name):
    name = ctx.message.content.removeprefix(".manga ")
    anime_dict = anilist.get_manga(name)
    desc = anime_dict['desc']
    embed = discord.Embed(
        colour=discord.Colour.light_blue(),
        title=anime_dict['name_romaji'],
        description=anime_dict['name_english']
        )
    embed.set_footer(text=anime_dict['genres'])
    embed.set_thumbnail(url=anime_dict['cover_image'])
    embed.set_image(url=anime_dict["banner_image"])
    chapters = anime_dict['chapters']
    volumes = anime_dict['volumes']
    match (chapters, volumes):
        case (None, None):
            info = "Info unavailable"
        case (chapters, None):
            info = f"Chapters: {chapters}"
        case (None, volumes):
            info = f"Volumes: {volumes}"
        case (chapters, volumes):
            info = f"Chapters: {chapters}\nVolumes: {volumes}"

    desc = ellipcise(markdownify(desc))
    embed.insert_field_at(0,name="Synopsis", value=desc, inline=True)
    embed.insert_field_at(0,name="Info", value=info, inline=True)
    print(anime_dict)

    await ctx.send(embed=embed)

@commands.command(
    brief="Search Anilist for a manga and post it's info in the chat"
)
async def anime(ctx, *name):
    name = ctx.message.content.removeprefix(".anime ")
    anime_dict = anilist.get_anime(name)
    desc = anime_dict['desc']
    embed = discord.Embed(
        colour=discord.Colour.dark_red(),
        title=anime_dict['name_romaji'],
        description=anime_dict['name_english']
        )
    embed.set_footer(text=anime_dict['genres'])
    embed.set_thumbnail(url=anime_dict['cover_image'])
    embed.set_image(url=anime_dict['banner_image'])

    episodes = anime_dict['airing_episodes']
    season = anime_dict['season'].capitalize()

    match (episodes, season):
        case (None, None):
            info = "Info unavailable"
        case (episodes, None):
            info = f"Episodes: {episodes}"
        case (None, season):
            info = f"Season: {season}"
        case (episodes, season):
            info = f"Episodes: {episodes}\nSeason: {season}"

    desc = ellipcise(markdownify(desc))
    embed.insert_field_at(1,name="Synopsis", value=desc, inline=True)
    embed.insert_field_at(0,name="Info", value=info, inline=True)
    await ctx.send(embed=embed)

async def setup(bot):
   bot.add_command(fox)
   bot.add_command(manga)
   bot.add_command(anime)
