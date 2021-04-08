import discord
from discord.ext import commands


class Translators(commands.Cog):
   def __init__(self, client):
      self.client = client


   @commands.command()
   async def uwuify(self, ctx, *, content):
      return await ctx.send(content.replace('r', 'w').replace('l', 'w').replace('R', 'W').replace('L', 'W'))


   @commands.command()
   async def reverse(self, ctx, *, content):
      return await content[::-1]

      
def setup(client):
   client.add_cog(Translators(client))