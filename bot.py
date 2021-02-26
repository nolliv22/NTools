import discord
from discord.ext import commands

from bot_token import bot_token
import subprocess

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle,
                                activity=discord.Game("Bruh"))
    print("Connecté")

@bot.event
async def on_message(mes):
    if mes.content.startswith(bot.command_prefix):
        print(f"{mes.author.name} : {mes.content}")
        await bot.process_commands(mes)


@bot.command()
async def test(ctx):
    await ctx.send("Ok")

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(extension)
    await ctx.send("Rechargé", delete_after=2)


bot.load_extension("cogs.eval")
bot.load_extension("jishaku")

bot.run(bot_token)