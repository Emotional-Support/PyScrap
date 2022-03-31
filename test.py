import os
import discord
from discord.ext import commands
import dotenv

prefix = "py "
intents = discord.Intents().all()

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(
    command_prefix=prefix,
    activity=discord.Activity(type=discord.ActivityType.listening, name="Blue World By Mac Miller"),
    help_command=None,
    intents=intents,
    case_insensitive=True,
)


@bot.event
async def on_ready():
    print(f"Logged Into: {bot.user}")


@bot.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Silenced")
    if role is None:
        await ctx.guild.create_role(name="Silenced", permissions=discord.Permissions(0))
    num = 1
    while True:
        try:
            bot.move_role(ctx.guild, "Silenced", num)
            break
        except:
            num += 1
    await member.add_roles(role)
    embed = discord.Embed(description=f"Muted {member.mention} Indefinetly.")
    await ctx.channel.send(embed=embed)


@bot.command()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Silenced")
    if role is not None:
        member.remove_roles(role)
    else:
        await ctx.channel.send("Role Doesn't Exist?")


@bot.command()
async def role(ctx, user: discord.Member, role: discord.Role):
    if role not in user.roles:
        await user.add_roles(role)
        embed = discord.Embed(description=f"Given The {role.mention} Role To {user.mention}.")
    else:
        await user.remove_roles(role)
        embed = discord.Embed(description=f"Removed The {role.mention} Role From {user.mention}.")
    await ctx.channel.send(embed=embed)


bot.run(TOKEN)
