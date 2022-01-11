import aioschedule
import discord
import random
from discord.ext import commands, tasks

from .periodic import Periodic

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
        return aioschedule.every().day.at("00:00")

    async def periodic_task(self):
        if not self.waifus:
            self.reload_waifus()

        waifu = random.choice(list(self.waifus.items()))
        self.waifus.pop(waifu[0])
        await self.bot.get_channel(self.channel).send(f"Dzisiejszą dziewczynką dnia jest: {waifu[1]}")