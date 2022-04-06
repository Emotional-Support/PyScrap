import asyncio
import re
import disnake
from disnake.ext import commands
import pymongo
from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
MONGO = os.getenv("MONGO")
ORANGE = 0xFF5733
cluster = MongoClient(MONGO, serverSelectionTimeoutMS=5000)
db = "discord"
collection = "user_info"

prefix = "py "
intents = disnake.Intents().all()

bot = commands.Bot(
    command_prefix=prefix,
    activity=disnake.Activity(type=disnake.ActivityType.listening, name="Blue World By Mac Miller"),
    help_command=None,
    intents=intents,
    case_insensitive=True,
)

bot_cogs = ["cogs.core_cog", "cogs.course_cog"]


for cog in bot_cogs:
    bot.load_extension(cog)

if __name__ == "__main__":
    bot.run(TOKEN)
