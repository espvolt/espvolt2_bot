import os
import discord

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv


client = commands.AutoShardedBot(command_prefix='%', case_insensitive=True)


@client.before_invoke
async def log_handler(message):
    with open('./logs/log.txt', 'a') as f:
        f.write('{0} used {1} at {2} UTC\n'.format(message.author, message.command, datetime.utcnow()))


@client.event
async def on_ready():
    with open('./logs/log.txt', 'w+') as f:
        f.write('Host has opened logs at {} UTC\n\n'.format(datetime.utcnow()))

    print('Bot is ready')


for cog in os.listdir('./cogs'):
    if cog.endswith('.py'):
        client.load_extension('cogs.{}'.format(cog[:-3]))

load_dotenv('.env') # Create your own
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
client.run(DISCORD_BOT_TOKEN)

