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
import os

if not os.path.isfile("settings.json"):
    sys.exit("'settings.json' not found!")
else:
    with open("settings.json") as file:
        settings = json.load(file)

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Weatherreport', description='Gives a Weather report of the current situation of a location')
    async def weather(self,ctx):
        if ctx.message.content == "!weather":
            embed = discord.Embed(title="Error", description="!weather requires a location \n!weather <Location/City/Town>", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
            return
        city = str(ctx.message.content).replace("!weather ","").capitalize()
        
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+settings["API-token"])
            print("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+settings["API-token"])
            print(response)
            print(settings["API-token"])
        except:
            embed = discord.Embed(title="Error: 400", description="An External Error has occured!", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
            return
        #conversion to json
        jsondata = response.json()
        try:
            temperature = round(float(jsondata['main']['temp'])-273.15,2)
            humidity = round(float(jsondata['main']['humidity']))
            pressure = round(float(jsondata['main']['pressure']))
            wind = round(float(jsondata['wind']['speed'])*3.6)
            feelslike = round(float(jsondata['main']['feels_like'])-273.15,1)
            cloudcover = round(float(jsondata['clouds']['all']))
            
            try:
                rain = round(float(jsondata['rain']['1h']))
            except:
                rain = 0
            try:
                snow = round(float(jsondata['snow']['1h']))
            except:
                snow = 0
        
        except:
            embed = discord.Embed(title="Error: 404", description="The location you specified is not valid.", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
        #TMP Index
        if temperature >= 28:
            index_tmp = 4
        elif temperature >= 23:
            index_tmp = 3
        elif temperature >= 18:
            index_tmp = 1
        elif temperature >= 0:
            index_tmp = 1
        else:
            index_tmp = 0
        
        #HUM Index
        if humidity >= 70:
            index_hum = 2
        elif humidity >= 30:
            index_hum = 1
        else:
            index_hum = 0
        

        status_tmp_list=['Cold','Moderate','Pleasant','Warm','Hot']
        status_hum_list=['Dry','Comfortable','Humid']
        
        status_tmp = status_tmp_list[index_tmp]
        status_hum = status_hum_list[index_hum]
        
        temp_string_list = ['. The temperature is ', '. It is ', '. Today it feels ', '. Outside it is ', " Currently, it is "]
        temp_string = random.choice(temp_string_list)
        
        hum_string_list = [', and it feels ', ', the air feels ', ', the atmosphere is ']
        hum_string = random.choice(hum_string_list)
        
        embed = discord.Embed(title="Weather Report", description= temp_string + status_tmp + hum_string + status_hum + ".", color=0x1C9FF6)
        
        embed.add_field(name="Temperature", value=str(temperature)+"°C", inline=True)
        embed.add_field(name="Percieved Temp.", value=str(feelslike)+"°C", inline=True)
        embed.add_field(name="Humidity", value=str(humidity)+ "%", inline=True)
        
        embed.add_field(name="Cloud coverage", value=str(cloudcover)+ "%", inline=True)
        embed.add_field(name="Rain", value=str(rain)+ "mm/h", inline=True)
        embed.add_field(name="Snow", value=str(snow)+ "mm/h", inline=True)
        
        embed.add_field(name="Pressure", value=str(pressure)+ "mBar", inline=True)
        embed.add_field(name="Wind", value=str(wind)+ "kmh", inline=True)
        
        await ctx.send(content=None, embed=embed)
            
#Fucking Important
def setup(bot):
    bot.add_cog(Weather(bot))
