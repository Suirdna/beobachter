import discord
from configs import bot_config
import asyncio
from modules import getter
from discord.ext import commands, tasks
from datetime import datetime

class stream(commands.Cog):

    #◄███▓▒░░ SYSTEM ░░▒▓███►#

    @tasks.loop(minutes=55)
    async def check_stream(self):
        await asyncio.sleep(5);

    def __init__(self,client):
        self.client = client;
        self.name = bot_config.CLIENT_NAME;
        self.author = bot_config.CLIENT_AUTHOR;
        self.check_stream.start();

def setup(client):
    client.add_cog(stream(client));