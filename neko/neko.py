import discord
from discord.ext import commands
import random

cats = ["Siamese", "Persian", "Sphinx"]
catimg = "https://cdn.discordapp.com/avatars/993804277631963206/3071341d6a3437a0572cf11d8a11f1c9.png?size=256?size=128"
catimgsad = "https://cdn.discordapp.com/attachments/1044500978973540374/1244213873955962930/tuCu6BT-_400x400.jpg?ex=66544bf7&is=6652fa77&hm=7ed639f6df0c2068c0576e2426371ef2ad02ae6c27511c399ea96132826d02ce&"
catimghappy = "https://cdn.discordapp.com/attachments/1044500978973540374/1244229154203897856/web_cat.jpg?ex=66545a33&is=665308b3&hm=032ecba7d6c53c9287a00079bbbc228ada32ba2b8859cddd83b7c885a258a2e4&"


class ViewDesu(discord.ui.View):

    foo: bool = None

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True

    async def on_timeout(self) -> None:
        timeoutembed = discord.Embed(title="Out of time! The cat left...")
        timeoutembed.insert_field_at(
            0,
            name="You have to do something or the cat will get bored!",
            value="You can feed the cat to befriend it or ignore the cat... if you'd like :pouting_cat:",
        )
        timeoutembed.set_thumbnail(url=catimg)
        await self.disable_all_items()
        await self.message.edit(embed=timeoutembed, view=self)

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
            embedfed.set_thumbnail(url=catimghappy)
        else:
            embedfed.insert_field_at(
                0,
                name="The cat took the food and ran off into the distance....",
                value="Better luck next time!",
            )
            embedfed.set_thumbnail(url=catimghappy)
        await interaction.response.edit_message(embed=embedfed, view=None)
        self.foo = True
        self.stop()

    @discord.ui.button(label="Ignore", style=discord.ButtonStyle.red)
    async def Ignore(self, interaction: discord.Interaction, button: discord.ui.button):
        foo: bool = None
        embedignored = discord.Embed(title="You ignored the cat...")
        embedignored.set_thumbnail(url=catimgsad)
        embedignored.insert_field_at(
            0,
            name="The cat went off into the distance",
            value="Type `.neko` again for a different cat... maybe this time you won't ignore it!",
        )
        await interaction.response.edit_message(embed=embedignored)
        self.foo = False
        self.stop()


@commands.command()
async def neko(ctx):
    embed = discord.Embed(
        title="Neko", description=f"A wild {random.choice(cats)} appeared!"
    )
    embed.set_thumbnail(url=catimg)
    embed.insert_field_at(0, name="What do you want to do?", value="Stats:\n")
    view = ViewDesu(timeout=3)
    message = await ctx.send(embed=embed, view=view)
    view.message = message
    await view.wait()
    await view.disable_all_items()

    if view.foo is None:
        print("Timeout")
    elif view.foo is True:
        print("Ok")
    else:
        print("Ignored")


async def setup(bot):
    bot.add_command(neko)
