import os
import discord
import time
from dotenv import load_dotenv
load_dotenv()
from utils import default
from utils.data import Bot, HelpFormat
from datetime import datetime
from pretty_help import DefaultMenu, PrettyHelp
#define things here
color = discord.Color.from_rgb(255,255,255)
token = os.getenv("TOKEN")
config = default.config() #used for the things in the config like loading prefixes
print("Logging in...")
#for pretty help
menu = DefaultMenu('◀️', '▶️', '❌') #used for menu nav

#defines bot for the "bot.run()" at the bottom, and for loading cogs
bot = Bot(
    command_prefix=config["prefix"], prefix=config["prefix"],
    owner_ids=config["devperms"], command_attrs=dict(hidden=True), help_command=HelpFormat(),
    allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False),
    intents=discord.Intents(
        guilds=True, members=True, messages=True, reactions=True, presences=True
    )
)

bot.help_command = PrettyHelp(navigation=menu, color=color)

#loads cogs
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

#logs into bot using the token stored in the .env file
try:
    bot.run(token)
except Exception as e:
    print(f"Error when logging in: {e}")


