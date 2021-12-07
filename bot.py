from discord.ext import commands
from discord.utils import get
import discord
import subprocess
import asyncio
import os
import sys

if not os.path.isfile("settings.json"):
    sys.exit("'settings.json' not found!")
else:
    with open("settings.json") as file:
        settings = json.load(file)

bot = commands.Bot(command_prefix=settings[prefix])
bot.remove_command('help')

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

@bot.event
async def on_ready():
    print("WeatherBot is online!, Beep Boop")
    activity = discord.Activity(name="I can tell you the weather, " + settings[prefix] + "help for info!", type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)

bot.run(settings[token])

























