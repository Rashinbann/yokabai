import discord
from discord.ext import commands
import random
import catstats
import json

state = {}


def get_state(key):
    return state.get(key)


def set_state(key, val):
    state[key] = val


class ViewDesu(discord.ui.View):

    foo: bool = None

    async def on_timeout(self) -> None:
        timeoutembed = discord.Embed(title="Out of time! The cat left...")
        timeoutembed.insert_field_at(
            0,
            name="You have to do something or the cat will get bored!",
            value="You can feed the cat to befriend it or ignore the cat... if you'd like :pouting_cat:",
        )
        timeoutembed.set_thumbnail(url=catstats.catimg)
        await self.message.edit(embed=timeoutembed, view=None)

    @discord.ui.button(label="Feed", style=discord.ButtonStyle.success)
    async def Feed(self, interaction: discord.Interaction, button: discord.ui.button):
        embedfed = discord.Embed(title="You fed the cat!")
        friending = random.uniform(0, 1)
        if friending < 0.70:
            embedfed.insert_field_at(
                0,
                name="You're my frind now!",
                value="The cat is now your friend! You can have soft tacos later!",
            )
            embedfed.set_thumbnail(url=catstats.catimghappy)
        else:
            embedfed.insert_field_at(
                0,
                name="The cat took the food and ran off into the distance...",
                value="Better luck next time!",
            )
            embedfed.set_thumbnail(url=catstats.catimghappy)
        await interaction.response.edit_message(embed=embedfed, view=None)
        self.foo = True
        self.stop()

    @discord.ui.button(label="Ignore", style=discord.ButtonStyle.red)
    async def Ignore(self, interaction: discord.Interaction, button: discord.ui.button):
        foo: bool = None
        embedignored = discord.Embed(title="You ignored the cat...")
        embedignored.set_thumbnail(url=catstats.catimgsad)
        embedignored.insert_field_at(
            0,
            name="The cat went off into the distance",
            value="Type `.neko` again for a different cat... maybe this time you won't ignore it!",
        )
        await interaction.response.edit_message(embed=embedignored, view=None)
        self.foo = False
        self.stop()


@commands.command()
async def neko(ctx):
    set_state("chosen_cat", random.choice(catstats.cats))
    set_state("stats", catstats.cat_map[get_state("chosen_cat")])

    embed = discord.Embed(
        title="Neko", description=f"A wild {get_state('chosen_cat')} cat appeared!"
    )
    embed.set_thumbnail(url=catstats.catimg)
    embed.insert_field_at(
        0,
        name="What do you want to do?",
        value=f"Strength: {get_state('stats')['Strength']}\nHealth: {get_state('stats')["Health"]}\nAgility: {get_state('stats')["Agility"]}",
    )
    view = ViewDesu(timeout=30)
    message = await ctx.send(embed=embed, view=view)
    view.message = message
    await view.wait()

    if view.foo is None:
        print("Timeout")
    elif view.foo is True:
        print("Ok")
    else:
        print("Ignored")


async def setup(bot):
    bot.add_command(neko)
