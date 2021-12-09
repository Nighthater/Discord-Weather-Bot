from discord.ext import commands
from discord.utils import get
import discord
import sys
import subprocess
import asyncio
import datetime
import re
import random
import requests
import json
import platform
import os

if not os.path.isfile("settings.json"):
    sys.exit("'settings.json' not found!")
else:
    with open("settings.json") as file:
        settings = json.load(file)

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


	#Hi
    @commands.command(brief='Says Hi', description='Friendly Hello :)')
    async def hi(self,ctx):
        await ctx.send("Hi!")

	#Displays Info about the Bot
    @commands.command(brief='Some Info about me', description='No additional info avalible',pass_context=True)
    async def about(self,ctx):
        uptime = ""
        
        #Uptime Script
        try:
            f = open( "/proc/uptime" )
            contents = f.read().split()
            f.close()
        except:
           uptime="404 Uptime not found :/"
     
        total_seconds = float(contents[0])
     
        # Helper vars:
        MINUTE  = 60
        HOUR    = MINUTE * 60
        DAY     = HOUR * 24
     
        # Get the days, hours, etc:
        days    = int( total_seconds / DAY )
        hours   = int( ( total_seconds % DAY ) / HOUR )
        minutes = int( ( total_seconds % HOUR ) / MINUTE )
        seconds = int( total_seconds % MINUTE )
     
        # Build up the string like this: "N days, N hours, N minutes, N seconds"
        string = ""
        if days > 0:
            string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
        if len(string) > 0 or hours > 0:
            string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
        if len(string) > 0 or minutes > 0:
            string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
        string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
     
        uptime = string
        

        embed = discord.Embed(title="About the Bot", description="", color=0x1C9FF6)
        embed.add_field(name="GitHub", value="https://github.com/Nighthater/Discord-Weather-Bot",inline=True)
        embed.add_field(name="Bot Version", value="1.0",inline=False)
        embed.add_field(name="Python version", value=platform.python_version(),inline=True)
        embed.add_field(name="Weather Data", value="OpenWeather API \nhttps://openweathermap.org",inline=True)
        embed.add_field(name="Current Server Time", value=datetime.datetime.now(),inline=False)
        embed.add_field(name="Host Server Uptime", value=uptime,inline=True)
        embed.add_field(name="Prefix", value=settings["prefix"],inline=True)
        await ctx.send(content=None, embed=embed)

    #Outputs User feedback into a file
    @commands.command(brief='Send feedback', description='Usage: '+settings["prefix"]+'feedback <Your message here>')
    async def feedback(self,ctx):
        if ctx.message.content == settings["prefix"] + "feedback":
            embed = discord.Embed(title="Error", description=settings["prefix"]+"feedback requires a message \n"+settings["prefix"]+"feedback <Your Message here>", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
            return
        print("Time: ", datetime.datetime.now(), file=open("logs/feedback.txt", "a"))
        print("Content: ", ctx.message.content, file=open("logs/feedback.txt", "a"))
        print("User: ", ctx.message.author, "\n", file=open("logs/feedback.txt", "a"))
        embed = discord.Embed(title="Feedback", description="Your feedback was succsessfully saved!", color=0x1C9FF6)
        await ctx.send(content=None, embed=embed)

    @commands.command(brief='Opens this Window', description='No additional Info avalible')
    async def help(self,ctx):
        embed = discord.Embed(title="Help", description="All Commands are listed here.", color=0x1C9FF6)
        embed.add_field(name='\u200b', value="Weather", inline=False)
        embed.add_field(name=settings["prefix"]+"weather [City or Location]", value="Lets you see the current weather on the location you specified", inline=False)
        embed.add_field(name=settings["prefix"]+"forecast [City or Location]", value="Lets you see the weather forecast for the next 24 hours on the location you specified", inline=False)
        embed.add_field(name=settings["prefix"]+"rain [City or Location]", value="Gives you a quick status message about incoming rain", inline=False)
        embed.add_field(name=settings["prefix"]+"air [City or Location]", value="Returns a list of the current Gases and Particle concentrations in the air", inline=False)
        embed.add_field(name=settings["prefix"]+"about", value="Info about the Bot", inline=False)
        embed.add_field(name=settings["prefix"]+"feedback [Your message]", value="Send Feedback, Questions or anything else regarding the bot", inline=False)
        
        #Footer
        
        await ctx.send(content=None, embed=embed)
            
def setup(bot):
    bot.add_cog(System(bot))
