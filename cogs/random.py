import discord
from discord.ext import commands
import random


class Random(commands.Cog):
   def __init__(self, client):
       self.client = client


   @commands.command()
   async def roll(self, ctx, sides=100):
      await ctx.send('{0} rolled {1}'.format(ctx.author.name, random.randint(1, sides)))


   @commands.command()
   async def randint(self, ctx, a: str, b: str):
      if not a.isdigit():
         return await ctx.send('Parameter `a` is not an integer')

      if not b.isdigit():
         return await ctx.send('Parameter `b` is not an integer')

      return await ctx.send('You got {}'.format(random.randint(int(a), int(b))))

   
   @commands.command()
   async def randchoice(self, ctx, *args):
      return await ctx.send('You got {}'.format(random.choice(args)))


   @commands.command(aliases=['rps'])
   async def rock_paper_scissors(self, ctx, user_input=''):
      possible_outcomes = {
         'rock': {
            'r': 'it\'s a tie',
            'p': 'you win',
            's': 'i win'
         },
         'paper': {
            'r': 'i win',
            'p': 'it\'s a tie',
            's': 'you win'
         },
         'scissors': {
            'r': 'you win',
            'p': 'i win',
            's': 'it\'s a tie'
         }
      }

      user_input = user_input.lower()
      possible_inputs = ['r', 'p', 's', 'rock', 'paper', 'scissors']

      if not user_input in possible_inputs:
         return await ctx.send('Input not valid must be {}'.format(','.join(possible_inputs)))

      choice = random.choice(list(possible_outcomes.keys()))
      laser_chance = random.random()

      if laser_chance <= .02:
         return await ctx.send('I choose laser, i win.')

      return await ctx.send('I choose {0}, {1}'.format(choice, possible_outcomes.get(choice).get(user_input[0])))


def setup(client):
   client.add_cog(Random(client))