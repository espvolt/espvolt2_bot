import discord
from discord.ext import commands
import random


class Random(commands.Cog):
   def __init__(self, client):
       self.client = client


   @commands.command()
   async def roll(self, ctx, sides=100):
      await ctx.send('{0} rolled {1}'.format(ctx.author.name, random.randint(1, sides)))


def setup(client):
   client.add_cog(Random(client))