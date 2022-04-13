import disnake
from disnake.ext import commands
import asyncio
from main import collection, ORANGE
from disnake.ui import Select, View
from disnake import SelectOption

install_confirm_react = ["✅"]


async def stage_one(bot: commands.Bot, ctx: commands.Context):
    select = Select(
        placeholder="Choose Your IDE",
        options=[
            SelectOption(
                label="Visual Studio Code",
                emoji="🔷",
                description="An IDE That Can Be Used With Any Language (Recommended)",
                value="vsc",
            ),
            SelectOption(label="PyCharm", emoji="🔶", description="An IDE Built Solely For Python", value="pycharm"),
        ],
    )

    async def callback(interaction: disnake.Interaction):
        if select.values[0] == "vsc":
            embed = disnake.Embed(
                title="Visual Studio Code",
                description="""
Click on this link to install:
https://code.visualstudio.com/Download
""",
            )
        elif select.values[0] == "pycharm":
            embed = disnake.Embed(
                title="PyCharm",
                description="""
Click on this link to install:
https://www.jetbrains.com/pycharm/download/#section=windows
""",
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    select.callback = callback
    view = View()
    view.add_item(select)

    embed = disnake.Embed(
        title="Checkpoint!", description="React to this embed once you finish installing your IDE and python", color=ORANGE
    )

    msg = await ctx.channel.send(embed=embed)

    def check_install(reaction, message):
        return message.author == ctx.author and reaction.emoji == "✅"

    user, reaction = bot.wait_for("reaction_add", timeout=600.0, check=check_install)

    if user == ctx.author and reaction == "✅":
        embed = disnake.Embed(
            title="Humble beginnings!",
            description='To begin your python journey, you need to install an "IDE" to write python code, and python itself!. Start by installing python:.',
            color=ORANGE,
        )
        embed.add_field(name="Python (required)", value="https://www.python.org/downloads/", inline=False)
        await ctx.channel.send(embed=embed, view=view)

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


async def stage_two(bot: commands.Bot, ctx: commands.Context):
    pass


async def stage_three(bot: commands.Bot, ctx: commands.Context):
    pass


async def stage_four(bot: commands.Bot, ctx: commands.Context):
    pass


async def stage_five(bot: commands.Bot, ctx: commands.Context):
    pass
