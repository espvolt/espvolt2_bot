import discord
import random
import asyncio

from discord.ext import commands


class Card:
    def __init__(self):
        percentage = random.random()

        colors = ['red', 'yellow', 'blue', 'green']
        self.color = random.choice(colors)

        if percentage <= .08:
            self.color = 'wildcard'
            self.action = random.randint(4, 5)
            self.value = 0

        elif percentage <= .30:
            self.action = random.randint(1, 3)
            self.value = 0
        
        else:
            self.action = 0
            self.value = random.randint(1, 9)


async def message_all(users, content):
    res = {}
    for user in users:
        message = await user.send(content)
        res[user.id] = message

    return res    


async def uno(client, players):
    players = [await client.fetch_user(int(playerID)) for playerID in players]
    in_game = players
    player_dict = {}

    for player in players:
        player_dict[player] = [Card() for i in range(7)] # Gives the player 7 cards

    top_card = Card()
    action = top_card.action

    messages = await message_all(players, 'Hi') # i plan on editing messages makes everything look better 
    # less pings if you dont want to watch the game no more
    
    # iterate over messages to edit all of them.
    
    while not len(in_game) in (0, 1): # makes sure the game has players
        await asyncio.sleep(1000) # prevents crashes
