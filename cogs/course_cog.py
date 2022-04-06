import disnake
from disnake.ext import commands
import asyncio
import re

from pyparsing import col
from main import cluster, db, collection, ORANGE, MongoClient

install_confirm_react = ["✅"]


async def stage_one(bot: commands.Bot, ctx: commands.Context):
    embed = disnake.Embed(
        title="Humble beginnings!",
        description='To begin your python journey, you need to install an "IDE" to write python code, and python itself!. Install python and one of these IDEs to get started.',
        color=ORANGE,
    )
    embed.add_field(name="Python (required)", value="https://www.python.org/downloads/", inline=False)
    embed.add_field(name="Visual Studio Code (IDE)", value="https://code.visualstudio.com/Download", inline=False)
    embed.add_field(name="PyCharm (IDE)", value="https://www.jetbrains.com/pycharm/download/#section=windows", inline=False)
    install_msg = await ctx.channel.send(embed=embed)

    await install_msg.add_reaction("✅")

    def check_install(reaction, user):
        return user == ctx.author and str(reaction.emoji) in install_confirm_react

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=600.0, check=check_install)
    except asyncio.TimeoutError:
        embed = disnake.Embed(
            title="Timed out!",
            description="You have taken too long to reply. Closing this session.",
            color=ORANGE,
        )
        await ctx.channel.send(embed=embed)
    else:
        if user == ctx.author:
            embed = disnake.Embed(
                title="Progress :sparkles:",
                description="Once you open your IDE, you can start writing your first line of code!",
                color=ORANGE,
            )
            embed.add_field(
                name="Step 1:", value="Create a new file called `main.py` and open it in your IDE with `ctrl o`", inline=False
            )
            embed.add_field(
                name="Step 2:",
                value="""
Enter this line of code into your IDE and press `ctrl f5` to run it
`print("hello world")`
""",
                inline=False,
            )
            await ctx.channel.send(embed=embed)


class CourseCog(commands.Cog):
    def __init__(self, bot: commands.Bot, cluster: MongoClient):
        self.bot = bot
        self.cluster = cluster
        self.db = self.cluster[db]
        self.collection = self.db[collection]

    @commands.command()
    async def course(self, ctx: commands.Context):
        user = self.collection.find_one({"_id": ctx.author.id})
        if user is not None:
            stage = user["level"]
            if stage >= 1:
                await stage_one(self.bot, ctx)
        else:
            embed = disnake.Embed(
                title="Oops!",
                description="You Haven't Registered With The Bot Yet. Run `py start` To Begin Your Python Journey :)",
                color=ORANGE,
            )
            await ctx.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CourseCog(bot, cluster))
