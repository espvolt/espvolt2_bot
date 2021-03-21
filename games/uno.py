import discord
import random

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


class Hand:
    def __init__(self):
        self.hand = [Card() for i in range(7)]

    def draw_card(self):
        self.hand.append(Card())


async def uno():
    # do uno stuff
    pass
