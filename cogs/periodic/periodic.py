import discord
from discord.ext import commands, tasks
from discord.utils import get
import aioschedule
import asyncio
import threading
from time import sleep

class Periodic(commands.Cog):
    """
        Cog that periodically performs a task.
    """
    def __init__(self, bot:discord.ext.commands.Bot):
        self.bot = bot
        self.channel = None #TODO: load previosly set from db
        self.scheduler_running = None

        name = type(self).__name__.lower()
        bot.command(name="schedule_"+name, pass_context=True, hidden=True)(self.schedule)
        bot.command(name="unschedule_" + name, pass_context=True, hidden=True)(self.unschedule)

    
    async def cog_check(self, ctx):
        #Check if user has manage messages perm
        return ctx.author.guild_permissions.manage_messages

    def period(self):
        return aioschedule.every(3).seconds

    def run_scheduler(self):
        """ Create the scheduler task. """
        async def _run_scheduler():
            self._scheduler_running = True
            while self._scheduler_running:
                await aioschedule.run_pending()
                await asyncio.sleep(1)

        if not self.scheduler_running:
            asyncio.create_task(_run_scheduler())

    async def periodic_task(self):
        await self.bot.get_channel(self.channel).send("Test")

    async def schedule(self, ctx):
        """Set this channel for a periodic task"""
        self.channel = ctx.message.channel.id
        self.period().do(self.periodic_task)
        self.run_scheduler()
        await ctx.send('Scheduled a task on this channel!')

    async def unschedule(self, ctx):
        """Stops periodic task"""
        self._scheduler_running = False
        await ctx.send('Unscheduled a task on this channel!')