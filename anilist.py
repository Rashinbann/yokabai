#!/usr/bin/python

import requests
import discord
from discord.ext import commands
from AnilistPython import Anilist
import textwrap
import re

anilist = Anilist()

def ellipcise(text):
    return textwrap.shorten(text, width=1024, placeholder="...")

markdown_map = [
    {'tag': ['<i>', '</i>'], 'markdown': '*'},
    {'tag': ['<b>', '</b>'], 'markdown': '**'},
    {'tag': '<br>', 'markdown': '\n\n'}

]

def convert_to_markdown(text, replace_map):
    for replacement in replace_map:
        tag = replacement['tag']
        markdown = replacement['markdown']

        if isinstance(tag, list):
            for t in tag:
                text = text.replace(t, markdown)
        elif isinstance(tag, str):
            text = text.replace(tag, markdown)
        else:
            raise TypeError(f"tag must be of type 'list' or 'str', was {type(tag)}")

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
    try:
        anime_dict = anilist.get_manga(name)
    except IndexError:
        await ctx.send("Manga is not found, try a different name.")
    else:
        desc = anime_dict['desc']
        embed = discord.Embed(
            colour=discord.Colour.blue(),
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
        embed.insert_field_at(1,name="Info", value=info, inline=True)
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
        colour=discord.Colour.dark_blue(),
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
    embed.insert_field_at(0,name="Synopsis", value=desc, inline=True)
    embed.insert_field_at(1,name="Info", value=info, inline=True)
    await ctx.send(embed=embed)

async def setup(bot):
   bot.add_command(fox)
   bot.add_command(manga)
   bot.add_command(anime)
