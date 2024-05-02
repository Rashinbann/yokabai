import requests
import discord
from discord.ext import commands
from AnilistPython import Anilist

anilist = Anilist()

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
        colour=discord.Colour.dark_red(),
        title=anime_dict['name_romaji'],
        description=anime_dict['name_english']
        )
    embed.set_footer(text=anime_dict['genres'])
    embed.set_thumbnail(url=anime_dict['cover_image'])

    # TO DO make it so that it doesn't actually print chapters/volumes if that info doesn't exist.
    # Right now it just gives None
    info = f"Chapters: {anime_dict['chapters']} \nVolumes: {anime_dict['volumes']}"
    embed.insert_field_at(0,name="Synopsis", value=desc, inline=True)
    embed.insert_field_at(2,name="Info", value=info, inline=True)
    print(anime_dict)
    lenght = len(anime_dict['desc'])
    if lenght < 1024:
        await ctx.send(embed=embed)
    else:
        await ctx.send('Desc is too long')

@commands.command(
    brief="Search Anilist for a manga and post it's info in the chat"
)
async def anime(ctx, *name):
    name = ctx.message.content.removeprefix(".anime ")
    anime_dict = anilist.get_anime(name)
    val = anime_dict.values()
    embed = discord.Embed(
        colour=discord.Colour.dark_red(),
        title=anime_dict['name_romaji'],
        description=anime_dict['name_english']
        )
    embed.set_footer(text=anime_dict['genres'])
    embed.set_thumbnail(url=anime_dict['cover_image'])
    # TO DO make it so that it doesn't actually print chapters/volumes if that info doesn't exist.
    # Right now it just gives None
    info = f"Episoodes: {anime_dict['airing_episodes']} \nSeason: {anime_dict['season']}"
    embed.insert_field_at(0,name="Synopsis", value=anime_dict['desc'], inline=True)
    embed.insert_field_at(2,name="Info", value=info, inline=True)
    print(anime_dict)
    await ctx.send(embed=embed)

async def setup(bot):
   bot.add_command(fox)
   bot.add_command(manga)
   bot.add_command(anime)