import discord
from discord.ext import commands
import random

cats = ["Siamese", "Persian", "Sphinx"]
catimg = "https://cdn.discordapp.com/avatars/993804277631963206/3071341d6a3437a0572cf11d8a11f1c9.png?size=256?size=128"


class ViewDesu(discord.ui.View):
    @discord.ui.button(label="Feed", style=discord.ButtonStyle.success)
    async def Feed(self, interaction: discord.Interaction, button: discord.ui.button):
        embedfed = discord.Embed(title="You fed the cat!")
        friending = random.choice([True, False])
        if friending is True:
            embedfed.insert_field_at(
                0,
                name="You're my frind now!",
                value="The cat is now your friend! You can have soft tacos later!",
            )
        else:
            embedfed.insert_field_at(
                0,
                name="The cat took the food and ran off into the distance....",
                value="Better luck next time!",
            )
        await interaction.response.edit_message(embed=embedfed)

    @discord.ui.button(label="Ignore", style=discord.ButtonStyle.red)
    async def Ignore(self, interaction: discord.Interaction, button: discord.ui.button):
        embedignored = discord.Embed(title="You ignored the cat...")
        embedignored.set_thumbnail(url=catimg)
        embedignored.insert_field_at(
            0,
            name="The cat went off into the distance",
            value="Type `.neko` again for a different cat... maybe this time you won't ignore it!",
        )
        await interaction.response.edit_message(embed=embedignored)


@commands.command()
async def neko(ctx):
    embed = discord.Embed(
        title="Neko", description=f"A wild {random.choice(cats)} appeared!"
    )
    embed.set_thumbnail(url=catimg)
    embed.insert_field_at(0, name="What do you want to do?", value="Stats:\n")
    embedfed = discord.Embed(title="You fed the cat!")
    view = ViewDesu()
    await ctx.send(embed=embed, view=view)


async def setup(bot):
    bot.add_command(neko)
