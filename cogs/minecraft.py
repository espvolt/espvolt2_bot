import discord
import json

from mcstatus import MinecraftServer
from discord.ext import commands


class Minecraft(commands.Cog):
   def __init__(self, client):
      self.client = client

   
   def parse_description(self, description: str):
      '''literally just remove all the color codes'''
      
      codes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'k', 'l', 'm'
               'n', 'o', 'r']

      for code in codes:
         
         description = description.replace('§{}'.format(code), '')

      return description


   @commands.command()
   async def save_server(self, ctx, common_ip, true_ip):
      '''mc status is kinda specific so hypixel doesn't work so we use this to ''Cache'' servers in a json'''

      with open('./jsons/common_servers.json', 'r+') as f:
         data = json.load(f)

         data[common_ip] = true_ip

         f.seek(0)
         f.truncate(0)
         json.dump(data, f, indent=4)
         

   @commands.command()
   async def mcserver(self, ctx, ip, port=25565):
      '''Thanks to dinnerbone for making the mcstatus library
      Only works with java'''

      with open('./jsons/common_servers.json', 'r+') as f:
         data = json.load(f)
      
      if ip in data:
         ip = data[ip]

      server = MinecraftServer.lookup('{0}:{1}'.format(ip, port))
      info = server.status()

      return await ctx.send(
         '```\n' +
         '{0}   {1} Players Online: {2}/{3}\n'.format(ip, info.version.name.replace('Requires MC ', ''), info.players.online, info.players.max) +
         '\n' +
         '{}'.format(self.parse_description(info.description)) +
         '```'
      )


def setup(client):
   client.add_cog(Minecraft(client))