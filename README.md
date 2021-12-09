# Discord-Weather-Bot

A simple Discord Bot you can edit and host yourself.
Uses discord.py as a framework and openweathermap.com API for free live weather data.


## Requirements:
- `Python 3.5.3` and up - https://www.python.org/downloads/
- `discord.py` - Using `pip install discord.py` will install the latest version. Read the Docs [here](https://discordpy.readthedocs.io/en/latest/).
- The Python code for the Bot itself - Download the latest [release](https://github.com/Nighthater/Discord-Weather-Bot/releases)


## Steps to use the bot yourself

### Configure settings.json

#### Get the API tokens:
- Create discord Bot token: https://discord.com/developers/applications
- Register on openweathermap.com and get an API key: https://home.openweathermap.org/users/sign_up

#### Replace `YOUR_PREFIX_HERE` with the Prefix you want to use the bot
- Common Prefixes are `_` `!` `?` `.`
- It is better to use a prefix that no other bot on your server already uses
#### Replace `YOUR_BOT_TOKEN_HERE` with your personal Discord Bot token
#### Replace `YOUR_OPENWEATHERMAP_API_TOKEN_HERE` with your personal API token from openweathermap.org

## Invite the bot to your server
- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Select your Application
- Select `OAuth2` then `URL Generator`
- Under `Scopes`, tick `bot`
- For `Permissions` you only need to tick `Send Messages` and `Read Message History`
- Open the generated URL at the bottom
- Select your server and confirm

## All done

Now you have finished setting up your bot.\
Run bot.py with `python3 bot.py` from the directory.
After a few seconds the bot should come online on your Server.
