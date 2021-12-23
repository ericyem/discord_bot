import os, discord
from dotenv import load_dotenv

def get_local_env(envString :str):
    pathname = os.path.abspath(envString)
    load_dotenv(dotenv_path=pathname)
    try:  
        bot_token=os.getenv("DISCORD_TOKEN")
    except KeyError: 
        print("Please set the environment variable bot_token")
        exit(1)
    return bot_token