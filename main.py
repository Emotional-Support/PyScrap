from ast import literal_eval as saferun
from numpy import safe_eval as safeeval
import asyncio
import re
import discord
from discord.ext import commands
import dotenv
import pymongo
from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
MONGO = os.getenv("MONGO")
ORANGE = 0xFF5733
cluster = MongoClient(MONGO, serverSelectionTimeoutMS=5000)
db = cluster["discord"]
collection = db["user_info"]

prefix = "py "
intents = discord.Intents().all()

bot = commands.Bot(
    command_prefix=prefix,
    activity=discord.Activity(type=discord.ActivityType.listening, name="Blue World By Mac Miller"),
    help_command=None,
    intents=intents,
    case_insensitive=True,
)


@bot.event
async def on_ready():
    print(f"Logged In As: {bot.user}")


@bot.event
async def on_guild_join(guild):
    for guild in bot.guilds:
        if collection.find_one({"_id": guild.id}) is None:
            collection.insert_one({"_id": guild.id})


@bot.event
async def on_message(message):
    if re.fullmatch(rf"<@!?{bot.user.id}>", message.content):
        embed = discord.Embed(
            title="Brrrrr",
            description="""
I'm PyScrap! A Discord Bot Created To Help People Learn Python.
You Can View My Commands With `py help`.

- Developed By `Emotional Support#3719` And `kabir#2505`.
""",
            color=ORANGE,
        )
        embed.set_image(url="https://media.giphy.com/media/igHg5yS08NvCwsvH0Z/giphy.gif")
        await message.channel.send(embed=embed)
    await bot.process_commands(message)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="List Of Commands: ", color=ORANGE)
    embed.add_field(
        name="Help Commands: ",
        value="""
`help`
""",
        inline=False,
    )
    embed.add_field(
        name="Tutorial Commands: ",
        value="""
`start`
""",
        inline=False,
    )
    await ctx.channel.send(embed=embed)


@bot.command()
async def start(ctx):
    collection.find_one({"_id": ctx.author.id})
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

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reacts

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="Timed Out!",
            description="You Have Taken Too Long To Reply. Closing This Session.",
            color=0xFF5733,
        )
        await ctx.channel.send(embed=embed)
    else:
        if user == ctx.author:
            if str(reaction.emoji) == "✅":
                embed = discord.Embed(title="Welcome!", description="Time To Begin Your Python Journey!", color=ORANGE)
                embed.add_field(
                    name="How Much Experience Do You Have With Python?",
                    value="""
1 - No Knowledge Of Python At All
2 - Slight Experience
3 - I Know Basic Python
""",
                )
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Goodbye :pensive:", description="We Hope You Can Join Us Next Time!", color=ORANGE
                )
                await ctx.channel.send(embed=embed)


if __name__ == "__main__":
    bot.run(TOKEN)
