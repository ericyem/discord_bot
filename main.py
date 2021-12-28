import discord
from utils import get_local_env
from bot.OgiBot import Ogikubot
import os

# don't change this code.
intents = discord.Intents.default()
intents.members = True
botClient = Ogikubot(command_prefix='$', intents=intents)
# runs the bot
botClient.run(os.getenv("TOKEN"))