from ast import literal_eval as saferun
import asyncio
import discord
from discord.ext import commands
import dotenv
from numpy import safe_eval as safeeval
import pymongo
from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

prefix = "py "
intents = discord.Intents().all()

bot = commands.Bot(
    command_prefix=prefix,
    activity=discord.Activity(type=discord.ActivityType.custom, name="Ok"),
    help_command=None,
    intents=intents,
    case_insensitive=True,
)


@bot.event
async def on_ready():
    print(f"Logged In As: {bot.user}")


@bot.command()
async def start(ctx):
    embed = discord.Embed(
        title="Begin Your Python Journey With PyScrap!",
        description="""Ever Wanted To Learn Python, But Never Knew Where To Start? 
        Well PyScrap Is The Bot For You! With This Course You'll Be A Python Expert In No Time!
        React To This Message To Continue :sparkling_heart:
""",
        color=0xFF5733,
    )
    bot_msg = await ctx.channel.send(embed=embed)
    await bot_msg.add_reaction("✅")
    await bot_msg.add_reaction("❎")

    valid_reacts = ["✅", "❎"]

    def check_yes(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reacts

    reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check_yes)
    if user == ctx.author:
        if str(reaction.emoji) == "✅":
            embed = discord.Embed(
                title="Welcome!",
                description="Time To Begin Your Python Journey!",
                color=0xFF5733,
            )
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Goodbye :pensive:",
                description="We Hope You Can Join Us Next Time!",
                color=0xFF5733,
            )
            await ctx.channel.send(embed=embed)


@start.error
async def on_start_error(ctx, error):
    embed = discord.Embed(
        title="Timed Out!",
        description="You Have Taken Too Long To Reply. Closing This Session.",
        color=0xFF5733,
    )
    if isinstance(error, asyncio.TimeoutError):
        await ctx.channel.send(embed=embed)


bot.run(TOKEN)
