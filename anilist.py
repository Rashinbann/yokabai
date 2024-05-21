#!/usr/bin/python

import requests
import discord
from discord.ext import commands
from AnilistPython import Anilist
import textwrap
import re
import datetime as dt
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
            raise TypeError(
                f"tag must be of type 'list' or 'str', was {type(tag)}")

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
async def parse_manga(data, ctx):
    name = ctx.message.content.removeprefix(".manga ")
    desc = data['desc']
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=data['name_romaji'],
        description=data['name_english']
    )
    embed.set_footer(text=data['genres'])
    embed.set_thumbnail(url=data['cover_image'])
    embed.set_image(url=data["banner_image"])
    mangaId = anilist.get_manga_id(name)
    embed.set_author(name="Go to page",
                     url=f"https://anilist.co/manga/{mangaId}")
    chapters = data['chapters']
    volumes = data['volumes']
    match (chapters, volumes):
        case (None, None):
            info = "Chapter info unavailable\n"
        case (chapters, None):
            info = f"Chapters: {chapters}"
        case (None, volumes):
            info = f"Volumes: {volumes}"
        case (chapters, volumes):
            info = f"Chapters: {chapters}\nVolumes: {volumes}\n"

    releaseFormat = data['release_format']
    releaseStatus = data['release_status']
    averageScore = data['average_score']
    startTime = data['starting_time']
    endTime = data['ending_time']
    info2 = f"Format: {releaseFormat}\nStatus: {releaseStatus}\nScore: {
        averageScore}\nStart Time: {startTime}\nEnd Time: {endTime}"
    if releaseStatus == "RELEASING":
        info2 = f"Format: {releaseFormat}\nStatus: {releaseStatus}\nScore: {
            averageScore}\nStart Time: {startTime}\n"
    desc = ellipcise(markdownify(desc))
    embed.insert_field_at(0, name="Synopsis", value=desc, inline=True)
    embed.insert_field_at(1, name="Info", value=info+info2, inline=True)

    await ctx.send(embed=embed)


@commands.command()
async def manga(ctx, *name):
    name = ctx.message.content.removeprefix(".manga ")
    try:
        anime_dict = anilist.get_manga(name)
    except IndexError:
        await ctx.send("Manga is not found, try a different name.")
    else:
        await parse_manga(anime_dict, ctx)


async def parse_anime(data, ctx):
    name = ctx.message.content.removeprefix(".anime ")
    data = anilist.get_anime(name)
    desc = data['desc']
    embed = discord.Embed(
        colour=discord.Colour.dark_blue(),
        title=data['name_romaji'],
        description=data['name_english']
    )
    embed.set_footer(text=data['genres'])
    embed.set_thumbnail(url=data['cover_image'])
    embed.set_image(url=data['banner_image'])
    aniId = anilist.get_anime_id(name)
    embed.set_author(name="Go to page",
                     url=f"https://anilist.co/anime/{aniId}")
    episodes = data['airing_episodes']



    season = data['season'] or "Unavailable"
    season = season.capitalize()
    # TODO: Deal with "Not Yet Released" anime and manga w
    # This code sucks ass and I have no idea how to deal with that
    # Good luck future me LMAO

    airingStatus = data['airing_status']
    airingFormat = data['airing_format']
    startingTime = data['starting_time']
    endingTime = data['ending_time']
    score = data['average_score']
    if airingStatus != "NOT_YET_RELEASED":
        match (episodes, season):
            case (None, None):
                info = "Episode info unavailable"
            case (episodes, None):
                info = f"Episodes: {episodes}"
            case (None, season):
                info = f"Season: {season}"
            case (episodes, season):
                info = f"Episodes: {episodes}\nSeason: {season}\n"

        info += f"Format: {airingFormat}\nStatus: {airingStatus}\nScore: {
            score}\nStart Date: {startingTime}\nEnd Date: {endingTime}"

    else:
        info = "Episode info unavailable"

    if airingStatus == "RELEASING":
        nextAiring = data['next_airing_ep']['timeUntilAiring']
        relativeAiringDays = dt.timedelta(seconds=nextAiring).days
        info += f"Next Episode In: {relativeAiringDays} day(s)\n"

    desc = ellipcise(markdownify(desc))
    desc = ellipcise(markdownify(desc))
    embed.insert_field_at(0, name="Synopsis", value=desc, inline=True)
    embed.insert_field_at(1, name="Info", value=info, inline=True)
    await ctx.send(embed=embed)


@commands.command(
    brief="Search Anilist for a manga and post its info in the chat"
)
async def anime(ctx, *name):
    name = ctx.message.content.removeprefix(".anime ")
    try:
        anime_dict = anilist.get_anime(name)
    except IndexError:
        await ctx.send("Anime is not found, try a different name.")
    else:
        await parse_anime(anime_dict, ctx)


async def setup(bot):
    bot.add_command(fox)
    bot.add_command(manga)
    bot.add_command(anime)
