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

if not os.path.isfile("settings.json"):
    sys.exit("'settings.json' not found!")
else:
    with open("settings.json") as file:
        settings = json.load(file)

class Rain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(brief='rain', description='gives information about incoming rain')
    async def rain(self,ctx):   
          
        if ctx.message.content == "!rain":
            embed = discord.Embed(title="Error", description="!rain requires a location \n!rain <Location/City/Town>", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
            return
        
        #Obtaining lat and lon from location specified
        city = str(ctx.message.content).replace("!rain ","").capitalize()
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+settings[API-token])
        except:
            embed = discord.Embed(title="Error: 400", description="An External Error has occured!", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
    
        jsondata = response.json()
        lat = str(jsondata['coord']['lat'])
        lon = str(jsondata['coord']['lon']) #Lat lon obtained!
        
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&appid="+settings[API-token])
        except:
            embed = discord.Embed(title="Error: 400", description="An External Error has occured!", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
        jsondata = response.json()
        
        #Minutely Data
        precipitation_data = []
        for i in range(0,60,1):
            precipitation_data.append(round(jsondata['minutely'][i]['precipitation'],1))
        
        
        mean = round(sum(precipitation_data))
        
        index_rain = next((index for index,value in enumerate(precipitation_data) if value != 0.0), None)
        

        embed = discord.Embed(title="Rain forecast for "+ city, color=0x1C9FF6)
        
        if index_rain == None:
            embed.add_field(name="Expected Rain", value="There will be no expected Rain in the next hour.", inline=False)
        elif index_rain < 1:
            index_over = next((index for index,value in enumerate(precipitation_data) if value == 0.0), None)
            if index_over == None:
                returnstring = "The Rain will not end within the next hour."
            else:
                returnstring = "The Rain will end in " + index_over + "minutes."
            
            embed.add_field(name="Expected Rain", value="It is already raining. \n"+returnstring, inline=False)
            embed.add_field(name="Total Rain", value=str(mean)+"mm of Rain will fall over the next hour.", inline=False)
        elif index_rain < 10:
            embed.add_field(name="Expected Rain", value="There is rain expected in less than 10 minutes.", inline=False)
            embed.add_field(name="Total Rain", value=str(mean)+"mm of Rain will fall over the next hour.", inline=False)
        else:
            embed.add_field(name="Expected Rain", value="There is rain expected in "+str(index_rain)+" minutes.", inline=False)
            embed.add_field(name="Total Rain", value=str(mean)+"mm of Rain combined will fall over the next hour", inline=False)
        await ctx.send(content=None, embed=embed)
        
def setup(bot):
    bot.add_cog(Rain(bot))
