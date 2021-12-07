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

class Air(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


	#Hi
    @commands.command(brief='Outputs Air Quality information', description='')
    async def air(self,ctx):
        if ctx.message.content == "!air":
            embed = discord.Embed(title="Error", description="!air requires a location \n!air <Location/City/Town>", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
            return
        
        #Obtaining lat and lon from location specified
        city = str(ctx.message.content).replace("!air ","").capitalize()
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+settings[API-token])
        except:
            embed = discord.Embed(title="Error: 400", description="An External Error has occured!", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
    
        jsondata = response.json()
        lat = str(jsondata['coord']['lat'])
        lon = str(jsondata['coord']['lon']) #Lat lon obtained!
        
        try:
            response = requests.get("http://api.openweathermap.org/data/2.5/air_pollution?lat="+lat+"&lon="+lon+"&appid="+settings[API-token])
        except:
            embed = discord.Embed(title="Error: 400", description="An External Error has occured!", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
        jsondata = response.json()
        
        
        AQI = round(jsondata['list'][0]['main']['aqi'])
        
        
        co = round(jsondata['list'][0]['components']['co'])
        no = round(jsondata['list'][0]['components']['no'],3)
        no2 = round(jsondata['list'][0]['components']['no2'],3)
        
        o3 = round(jsondata['list'][0]['components']['o3'])
        so2 = round(jsondata['list'][0]['components']['so2'],2)
        pm2_5 = round(jsondata['list'][0]['components']['pm2_5'],2)
        
        pm10 = round(jsondata['list'][0]['components']['pm10'],2)
        nh3 = round(jsondata['list'][0]['components']['nh3'],2)
        
        switcher={
        1:'Good',
        2:'Fair',
        3:'Moderate',
        4:'Poor',
        5:'Very Poor',
        }
        AQI_STRING = str(switcher.get(AQI,"- Invalid AQI -"))

        
        
        embed = discord.Embed(title="Air Quality Report", description='Overall, the air Quality is to be classified as '+AQI_STRING+".", color=0x1C9FF6)
        
        embed.add_field(name="Carbon Monoxide", value=str(co)+" μg/m³", inline=True)
        embed.add_field(name="Nitrogen Monoxide", value=str(no)+" μg/m³", inline=True)
        embed.add_field(name="Nitrogen Dioxide", value=str(no2)+" μg/m³", inline=True)
        
        embed.add_field(name="Ozone", value=str(o3)+" μg/m³", inline=True)
        embed.add_field(name="Sulphur Dioxide", value=str(so2)+" μg/m³", inline=True)
        embed.add_field(name="Ammonia", value=str(nh3)+" μg/m³", inline=True)
        
        embed.add_field(name="Fine Air Particles", value=str(pm2_5)+" μg/m³", inline=True)
        embed.add_field(name="Coarse Air Particles", value=str(pm10)+" μg/m³", inline=True)
        
        await ctx.send(content=None, embed=embed)
    
def setup(bot):
    bot.add_cog(Air(bot))
