import disnake
from disnake.ext import commands
import asyncio
import re
from main import cluster, db, collection, ORANGE, MongoClient

valid_reacts = ["✅", "❎"]
valid_reacts2 = ["😶", "😮", "😎"]
xp_list = ["1", "2", "3"]


class CoreCog(commands.Cog):
    def __init__(self, bot: commands.Bot, cluster: MongoClient):
        self.bot = bot
        self.cluster = cluster
        self.db = self.cluster[db]
        self.collection = self.db[collection]

    @commands.Cog.listener()
    async def on_message(self, message):
        if re.fullmatch(rf"<@!?{self.bot.user.id}>", message.content):
            embed = disnake.Embed(
                title="Brrrrr",
                description="""
I'm PyScrap! A disnake Bot Created To Help People Learn Python.
You Can View My Commands With `py help`.

- Developed By `Emotional Support#3719`.
        """,
                color=ORANGE,
            )
            embed.set_image(url="https://media.giphy.com/media/igHg5yS08NvCwsvH0Z/giphy.gif")
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged In As: {self.bot.user}")

    @commands.command()
    async def help(self, ctx: commands.Context):
        embed = disnake.Embed(title="List Of Commands: ", color=ORANGE)
        embed.add_field(
            name="Help Commands: ",
            value="""
    `help`
    """,
            inline=False,
        )
        embed.add_field(
            name="Course Commands: ",
            value="""
    `start` `course`
    """,
            inline=False,
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def start(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Begin Your Python Journey With PyScrap!",
            description="""Ever wanted to learn python, but never knew where to start? 
well pyscrap is the bot for you! With this course you'll be a python expert in no time!
React to this message to continue :sparkling_heart:
""",
            color=0xFF5733,
        )
        bot_msg1 = await ctx.channel.send(embed=embed)
        await bot_msg1.add_reaction("✅")
        await bot_msg1.add_reaction("❎")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reacts

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            embed = disnake.Embed(
                title="Timed Out!",
                description="You Have Taken Too Long To Reply. Closing This Session.",
                color=ORANGE,
            )
            await ctx.channel.send(embed=embed)
        else:
            if user == ctx.author:
                if str(reaction.emoji) == "✅":
                    user_db = self.collection.find_one({"_id": ctx.author.id})
                    if user_db is None:
                        self.collection.insert_one({"_id": ctx.author.id, "level": 0})
                        user_db = self.collection.find_one({"_id": ctx.author.id})

                    if user_db["level"] == 0:
                        embed = disnake.Embed(title="Welcome!", description="Time To Begin Your Python Journey!", color=ORANGE)
                        embed.add_field(
                            name="How much experience do you have with python?",
                            value="""
😶 - No knowledge of python at all
😮 - Slight experience
😎 - I know basic python
        """,
                        )
                        bot_msg2 = await ctx.channel.send(embed=embed)
                        await bot_msg2.add_reaction("😶")
                        await bot_msg2.add_reaction("😮")
                        await bot_msg2.add_reaction("😎")

                        def check2(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in valid_reacts2

                        try:
                            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check2)
                        except asyncio.TimeoutError:
                            embed = disnake.Embed(
                                title="Timed Out!",
                                description="You Have Taken Too Long To Reply. Closing This Session.",
                                color=0xFF5733,
                            )
                            await ctx.channel.send(embed=embed)
                        else:
                            if user == ctx.author:
                                embed = disnake.Embed(
                                    title="Congrats!",
                                    description="You have finished the tutorial! Yype `py course` to begin the course.",
                                    color=ORANGE,
                                )
                                if str(reaction.emoji) == "😶":
                                    self.collection.update_one({"_id": ctx.author.id}, {"$set": {"level": 1}})
                                elif str(reaction.emoji) == "😮":
                                    self.collection.update_one({"_id": ctx.author.id}, {"$set": {"level": 10}})
                                elif str(reaction.emoji) == "😎":
                                    self.collection.update_one({"_id": ctx.author.id}, {"$set": {"level": 15}})
                                await ctx.channel.send(embed=embed)
                    else:
                        embed = disnake.Embed(
                            title="Oops!",
                            description="""
    You've already finished the tutorial :D
    Run `py course` to begin/resume the course!
    """,
                            color=ORANGE,
                        )
                        await ctx.channel.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="Goodbye :pensive:", description="We Hope You Can Join Us Next Time!", color=ORANGE
                    )
                    await ctx.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot, cluster))
