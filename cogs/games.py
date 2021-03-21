import json
import discord

from discord.ext import commands
from games.uno import uno
# still working on it

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.games = {
            'uno': uno
        }


    @commands.command()
    async def play(self, ctx, game):
        authorID = ctx.author.id
        if not game.lower() in self.games:
            return await ctx.send('{} is not a game'.format(game))

        with open('./jsons/games.json', 'r+') as f:
            data = json.load(f)
 
            if str(authorID) in data:
                return await ctx.send('You already have a game queued')

            data[str(authorID)] = {
                'type': game.lower(),
                'players': []
            }

            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)

        return await ctx.send('You have started a game %start to begin.')

    
    @commands.command()
    async def join(self, ctx, user):
        userID = int(user[2:-1].replace('!', '')) # on mobile its a bit different for some reason, i would just use user[3:-1]
        authorID = ctx.author.id
        
        if userID == authorID:
            return await ctx.send('You can\'t join yourself')

        with open('./jsons/games.json', 'r+') as f:
            data = json.load(f)
            
            if not str(userID) in data:
                return await ctx.send('Could not find game')

            game_dict = data.get(str(userID))
            players = game_dict.get('players')

            if str(authorID) in players:
                return await ctx.send('You are already in this game.')

            game_dict['players'].append(str(authorID))

            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)


    @commands.command()
    async def start(self, ctx):
        authorID = ctx.author.id

        with open('./jsons/games.json', 'r+') as f:
            data = json.load(f)

            if not str(authorID) in data:
                return await ctx.send('You have no game to start')

            game_dict = data.get(str(authorID))
            players = [int(player) for player in game_dict.get('players')] # Since the player ID are string i turn them back to int but

            if len(players) == 0:
                return await ctx.send('Nobody has joined your game.') 
                
            players.insert(0, authorID) # authorID is already int so no need for int()

            game_type = game_dict.get('type')

            data.pop(str(authorID)) # removes the game from the json because its started
            
            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)

            await ctx.send('Your game has started')
            return await self.games.get(game_type)(self.client, players) # calls the function
            

def setup(client):
    client.add_cog(Games(client))