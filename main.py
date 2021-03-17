import os
import discord

from discord.ext import commands
from dotenv import load_dotenv


client = commands.AutoShardedBot(command_prefix='%', case_insensitive=True)


@client.event
async def on_ready():
    print('Bot is ready')
    

for cog in os.listdir('./cogs'):
    if cog.endswith('.py'):
        client.load_extension('cogs.{}'.format(cog[:-3]))

load_dotenv('.env') # Create your own
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
client.run(DISCORD_BOT_TOKEN)

