import aioschedule
import discord
import random
import requests
from discord.ext import commands, tasks
from xml.etree import ElementTree

from .periodic import Periodic

emojis = ['😍', '🥰', '😋', '😲', '👀', '❤️', '💓', '👌', '😳', '🥵']

class Waifu(Periodic):
    """
        Cog that randomizes a character from a list
    """
    def __init__(self, bot: discord.ext.commands.Bot):
        super(Waifu, self).__init__(bot)
        self.waifus = None

    # TODO: use database
    def reload_waifus(self):
        self.waifus = {'ganyu_(genshin_impact)': "Ganyu",
                  'shenhe_(genshin_impact)': "Shenhe",
                  'jean_(genshin_impact)': "Jean",
                  'lumine_(genshin_impact)': "Lumine"}

    def period(self):
        return aioschedule.every(10).seconds

    async def periodic_task(self):
        if not self.waifus:
            self.reload_waifus()

        waifu = random.choice(list(self.waifus.items()))
        self.waifus.pop(waifu[0])

        params = {"page":"dapi", "s":"post", "q":"index", "limit":50, "pid":0, "tags":waifu[0]+" solo"}
        r = requests.get(f"https://safebooru.org/index.php", params=params)
        posts = ElementTree.fromstring(r.content)

        await self.bot.get_channel(self.channel).send(f"Dzisiejszą dziewczynką dnia jest: **{waifu[1]}** {random.choice(emojis)}")
        await self.bot.get_channel(self.channel).send(f"{random.choice(posts).attrib['file_url']}")