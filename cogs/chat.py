import re
import discord
import json
import codecs

from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener('on_message')
    async def on_swear(self, message):
        authorID = message.author.id
        words = ['qvpx', 'shpx', 'fuvg', 'ovgpu', 'avttre', 'phag', 'onfgneq', 'fyhg', 'chffl', 'snttbg', 'juber', 'pbpx', 'ergneq', 'pbba']

        curse_count = 0

        for word in words:
            true_word = codecs.decode(word, 'rot-13') # uhhhhhh look teach might see this junk
            curse_array = re.findall(true_word, message.content.lower())
            
            curse_count += len(curse_array)

        if curse_count > 0: # dont want to save everyone to a json even if they dont even curse
            with open('./jsons/curse_counter.json', 'r+') as f:
                data = json.load(f)

                
                if str(authorID) in data:
                    n_curses = data.get(str(authorID)) + curse_count

                else:
                    n_curses = curse_count

                data[str(authorID)] = n_curses
                f.seek(0)
                f.truncate(0)
                json.dump(data, f, indent=4) 





def setup(client):
    client.add_cog(Chat(client))

