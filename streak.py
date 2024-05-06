from discord.ext import commands
import sqlite3
import discord

db = sqlite3.connect('streakdb.db')
cursor = db.cursor()

@commands.group(invoke_without_commmand=True)
async def streak(ctx):
     if ctx.invoked_subcommand is None:
        await ctx.send(f"To add a streak do `.streak add [your streak]`")


@streak.command(
    brief="Adds your streak to the database",
    description="This will also update your streak to the number that you set it to, if you already have one."
)
async def add(ctx, days : int):
    authorMember = ctx.author
    number = ctx.message.content.removeprefix(".streak add ")
    try:
        cursor.execute("SELECT streak FROM mytable WHERE user = ?", (author,))


        existing_streak = cursor.fetchone()

        if existing_streak is None:
            cursor.execute("INSERT INTO mytable(user, streak) VALUES(?, ?)", (author, number))
            await ctx.send("Streak added successfully")
        else:
            cursor.execute("UPDATE mytable SET streak = ? WHERE user = ?", (number, author))
            await ctx.send("Your streak hass been added! To update your streak incrementally you can do `.streak done`")

    finally:
        db.commit()
        cursor.close()
        db.close()


@streak.command(
    brief="Increments your current streak by 1"
)
async def done(ctx):
    authorMember = ctx.author
    identifier = authorMember.id()
    db = sqlite3.connect('streakdb.db')
    cursor = db.cursor()
    try:
        # Check if the user exists in the database
        cursor.execute("SELECT streak FROM mytable WHERE user = ?", (id,))


        existing_streak = cursor.fetchone()

        if existing_streak is None:
            # If the user doesn't exist
            await ctx.send("To add a streak do `.streak add [your streak]`")
        else:
            # If the user exists
            cursor.execute("UPDATE mytable SET streak = streak + 1 WHERE user = ?", (id,))
            await ctx.send("You done it")

    finally:
        db.commit()
        cursor.close()
        db.close()


@streak.command(
    brief="See all the streaks in the database"
)
async def see(ctx):
    authorMember = ctx.author
    db = sqlite3.connect('streakdb.db')
    cursor = db.cursor()
    cursor.execute("SELECT user, streak FROM mytable")
    data = cursor.fetchall()

    embed = discord.Embed(
        colour=discord.Colour.dark_red(),
        title="See streaks"
    )

    streak_info = ""
    for user, streak in data:
        streak_info += f"{user}: {streak}\n"

    embed.add_field(name="Streaks", value=streak_info, inline=False)

    await ctx.send(embed=embed)

    db.close()

@streak.command(
    brief="See your current streak"
)
async def seeme(ctx):
    authorMember = ctx.author
    identifier =  authorMember.id()
    db = sqlite3.connect('streakdb.db')
    cursor = db.cursor()
    cursor.execute("SELECT streak FROM mytable WHERE user =?", (id,))
    data = cursor.fetchone()
    datastr = str(data[0])

    await ctx.send(f"Your current streak is {datastr}")
async def setup(bot):
    bot.add_command(streak)