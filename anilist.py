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

    chapters = anime_dict['chapters']
    volumes = anime_dict['volumes']

    if chapters is None and volumes is None:
        info = "Info unavailable"
    else:
        if chapters:
            info += f"Chapters: {chapters}"
        if volumes:
            if chapters:
                info += "\n"
            info += f"Volumes: {volumes}"

    desc = textwrap.shorten(anime_dict['desc'], width=1024, placeholder="...")
    embed.insert_field_at(0,name="Synopsis", value=desc, inline=True)
    embed.insert_field_at(2,name="Info", value=info, inline=True)
    print(anime_dict)

    await ctx.send(embed=embed)

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
    episodes = anime_dict['airing_episodes']
    season = anime_dict['season']

    if episodes is None and season is None:
        info = "Info unavailable"
    else:
        if episodes:
            info += f"Episodes: {episodes}"
        if season:
            if episodes:
                info += "\n"
            info += f"Season: {season}"


    embed.insert_field_at(0,name="Synopsis", value=anime_dict['desc'], inline=True)
    embed.insert_field_at(2,name="Info", value=info, inline=True)
    print(anime_dict)
    await ctx.send(embed=embed)

async def setup(bot):
   bot.add_command(fox)
   bot.add_command(manga)
   bot.add_command(anime)