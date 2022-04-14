import asyncio
import re
import disnake
from disnake.ext import commands
import pymongo
from pymongo import MongoClient
import os
import dotenv
from disnake.ui import Select, View
from disnake import SelectOption

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
MONGO = os.getenv("MONGO")
ORANGE = 0xD2FF00
cluster = MongoClient(MONGO, serverSelectionTimeoutMS=300000)
db = "discord"
collection = "user_info"

prefix = "py "
intents = disnake.Intents().all()

bot = commands.Bot(
    command_prefix=prefix,
    activity=disnake.Activity(type=disnake.ActivityType.listening, name="`Loud` By Mac Miller"),
    help_command=None,
    intents=intents,
    case_insensitive=True,
)


@bot.command()
async def test(ctx: commands.Context):
    async def callback(interaction: disnake.Interaction):
        embed = disnake.Embed(title="Yooo", description=f"You chose {select.values[0]}", color=ORANGE)
        await interaction.response.send_message(embed=embed)

    select = Select(
        placeholder="Testing",
        options=[
            SelectOption(label="Test1", emoji="😎", description="Test2"),
            SelectOption(label="Test2", description="Test2", emoji="🥰"),
        ],
    )
    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.channel.send(view=view)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx: commands.Context, amt: int):
    await ctx.channel.purge(limit=amt)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context):
    cluster["discord"]["user_info"].delete_many({})
    await ctx.channel.send("Cleared Document!")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def poll(ctx: commands.Context, *, options: str):

    dict = {}
    total = 0
    list_ch = options.split("/")
    question = list_ch[0]
    list_ch.remove(question)
    choices = list_ch[0].split(",")

    embed = disnake.Embed(title=question, color=ORANGE)

    for ch in choices:
        embed.add_field(name=f"{ch}: ", value=f"{0}%", inline=False)
        dict.update({ch: 0})

    option_list = []

    select = Select(
        placeholder="Choose An Option",
        options=option_list,
    )

    for op in choices:
        option_list.append(SelectOption(label=op, value=op))

    async def callback(interaction: disnake.Interaction):

        nonlocal total
        total += 1
        dict[select.values[0]] += 1

        total_num = 0

        for l in dict.values():
            total_num += l

        embed = disnake.Embed(title=question, color=ORANGE)

        for ch in choices:
            percentage = dict[ch] // total_num * 100
            embed.add_field(name=f"{ch}:    ", value=f"{percentage}%", inline=False)

        await msg.edit(embed=embed)
        await interaction.response.defer()

    select.callback = callback
    view = View()
    view.add_item(select)
    msg = await ctx.channel.send(embed=embed, view=view)


bot_cogs = ["cogs.core_cog", "cogs.course_cog"]


for cog in bot_cogs:
    bot.load_extension(cog)

if __name__ == "__main__":
    bot.run(TOKEN)
