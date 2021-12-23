import discord
from utils import get_local_env
from OgiBot import Ogikubot   

# don't change this code.
intents = discord.Intents.default()
intents.members = True
bot_token = get_local_env("id.env")
botClient = Ogikubot(command_prefix='$', intents=intents)
botClient.run(bot_token)