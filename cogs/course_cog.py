import disnake
from disnake.ext import commands
import asyncio
import re
from main import cluster, db, collection, ORANGE, MongoClient
import stages.stage1_5 as stg1_5


class CourseCog(commands.Cog):
    def __init__(self, bot: commands.Bot, cluster: MongoClient):
        self.bot = bot
        self.cluster = cluster
        self.db = self.cluster[db]
        self.collection = self.db[collection]

    @commands.command()
    async def course(self, ctx: commands.Context):
        user = self.collection.find_one({"_id": ctx.author.id})
        if user is not None or user["level"] > 0:
            stage = user["level"]
            if stage == 1:
                await stg1_5.stage_one(self.bot, ctx)
            elif stage == 2:
                await stg1_5.stage_two(self.bot, ctx)
            elif stage == 3:
                await stg1_5.stage_three(self.bot, ctx)
            elif stage == 4:
                await stg1_5.stage_four(self.bot, ctx)
            elif stage == 5:
                await stg1_5.stage_five(self.bot, ctx)
        elif user is None or user["level"] == 0:
            embed = disnake.Embed(
                title="Oops!",
                description="You Haven't Registered With The Bot Yet. Run `py start` To Begin Your Python Journey :)",
                color=ORANGE,
            )
            await ctx.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CourseCog(bot, cluster))
