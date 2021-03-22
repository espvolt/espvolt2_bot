import discord
import json

from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def curses(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.author

        userID = user.id

        with open('./jsons/curse_counter.json', 'r+') as f:
            data = json.load(f)

            if str(userID) in data:
                curse_count = data.get(str(userID))
                return await ctx.send('{0} has cursed {1} times'.format(user.name, curse_count))

            else:
                return await ctx.send('{} has never cursed. What a good person'.format(user.name))


def setup(client):
    client.add_cog(Misc(client))