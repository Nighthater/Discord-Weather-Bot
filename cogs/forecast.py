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

#appids

class Forecast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='weatherreport', description='detail')
    async def forecast(self,ctx):
        if ctx.message.content == "!forecast":
            embed = discord.Embed(title="Error", description="!forecast requires a location \n!forecast <Location/City/Town>", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
            return
        
        city = str(ctx.message.content).replace("!forecast ","").capitalize()
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/forecast?q="+city+"&appid=")
        except:
            embed = discord.Embed(title="Error: 400", description="An External Error has occured!", color=0xFF0000)
            await ctx.send(content=None, embed=embed)
        #conversion to json
        jsondata = response.json()
        temp_list=[]
        temp_list_raw=[]
        hum_list_raw=[]
        status_list=[]
        timestamp_list=[]
        id_list=[]
        
        RainCounter = 0
        RainID=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        
        try:
            for i in range(0,9,1):
                temp_list.append(str(round(jsondata['list'][i]['main']['temp']-273.15,1))+" °C")
                
                temp_list_raw.append(round(jsondata['list'][i]['main']['temp']-273.15,1))
                hum_list_raw.append(round(jsondata['list'][i]['main']['humidity'])*100)
                
                icon_string = str(jsondata['list'][i]['weather'][0]['icon'])
                #Replaces id with emoji
                x = icon_string
                x = x.replace("01d",":sunny:")
                x = x.replace("01n",":sunny:")
                x = x.replace("02d",":white_sun_small_cloud:")
                x = x.replace("02n",":white_sun_small_cloud:")
                x = x.replace("03d",":white_sun_cloud:")
                x = x.replace("03n",":white_sun_cloud:")
                x = x.replace("04d",":cloud:")
                x = x.replace("04n",":cloud:")
                x = x.replace("09d",":white_sun_rain_cloud:")
                x = x.replace("09n",":white_sun_rain_cloud:")
                x = x.replace("10d",":cloud_rain:")
                x = x.replace("10n",":cloud_rain:")
                x = x.replace("11d",":thunder_cloud_rain:")
                x = x.replace("11n",":thunder_cloud_rain:")
                x = x.replace("13d",":snowflake:")
                x = x.replace("13n",":snowflake:")
                x = x.replace("50d",":rock:")
                x = x.replace("50n",":rock:")
                if 'rain' in str(jsondata['list'][i]['weather'][0]['description']):
                    status_list.append(x+" "+str(jsondata['list'][i]['weather'][0]['description']).capitalize()+" ("+str(round(float(jsondata['list'][i]['pop'])*100))+"%)")
                    RainID[RainCounter]= i
                    RainCounter = RainCounter + 1
                else:
                    status_list.append(x+" "+str(jsondata['list'][i]['weather'][0]['description']).capitalize() )
                tmpstring=str(jsondata['list'][i]['dt_txt'])
                timestamp_list.append(tmpstring[-8:-3]+"h")
                id_list.append(str(jsondata['list'][i]['weather'][0]['icon']))
        except:
            embed = discord.Embed(title="Error: 404", description="The location you specified is not valid.", color=0xFF0000)
            await ctx.send(content=None, embed=embed)

        
        
        intro_string_list = ['In the next hours it will be ','The weather for now will be ']
        intro_string = random.choice(intro_string_list)
        
        weather_stat_next_hours = jsondata['list'][1]['weather'][0]['description']
        
        rain_string_list = ['No Rain is expected for the next time. ', 'There seems to be a slight risk of Rain in the next time. ', 'There is a high risk of Rain in the next few hours. ']
        
        if(RainID[0] == 0 or RainID[0] == 1 or RainID[0] == 2 ):
            rain_decider = 2
        elif(RainID[0] == 3 or RainID[0] == 4 or RainID[0] == 5 ):
            rain_decider = 1
        else:
            rain_decider = 0
        rain_string = rain_string_list[rain_decider]
        
        
        Forecast_string = intro_string + weather_stat_next_hours + ". " + rain_string
        
        
        embed = discord.Embed(title="Weather Forecast for "+ city, description="The Weather forecast in "+city+" for the next 24 hours is as follows: \n" + Forecast_string, color=0x1C9FF6)
        embed.add_field(name="Temperature", value="\n".join(temp_list), inline=True)
        embed.add_field(name="Weather", value="\n".join(status_list), inline=True)
        embed.add_field(name="Time", value="\n".join(timestamp_list), inline=True)
        
        await ctx.send(content=None, embed=embed)
        

def setup(bot):
    bot.add_cog(Forecast(bot))
