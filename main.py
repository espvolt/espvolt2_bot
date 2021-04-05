import os
import discord

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv


client = commands.AutoShardedBot(command_prefix='%', case_insensitive=True)


def load_cogs(directory: str):
    if directory.startswith('./') and len(directory) != 2:
        directory = directory[2:]

    for cog in os.listdir(directory):
        current_dir = '{0}/{1}'.format(directory, cog)
        
        if os.path.isdir(current_dir):
            load_cogs(current_dir)

        else:
            if cog.endswith('.py'):
                extention_dir = current_dir.replace('/', '.')[:-3]

                client.load_extension(extention_dir)
                print('Loaded {}'.format(extention_dir))


@client.before_invoke
async def log_handler(message):
    with open('./logs/log.txt', 'a') as f:
        f.write('{0} used {1} at {2} UTC\n'.format(message.author, message.command, datetime.utcnow()))


@client.event
async def on_ready():
    with open('./logs/log.txt', 'w+') as f:
        f.write('Host has opened logs at {} UTC\n\n'.format(datetime.utcnow()))

    print('Bot is ready')

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="https://github.com/espvolt/espvolt2_bot")) 
    # stolen from https://stackoverflow.com/questions/59126137/how-to-change-discord-py-bot-activity


load_cogs('cogs')
load_dotenv('.env') # Create your own
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
client.run(DISCORD_BOT_TOKEN)