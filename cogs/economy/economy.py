import discord
from discord.ext import commands

from .EconomySystem import EconomySystem

from decimal import *


class Economy(commands.Cog):
    def __init__(self, bot, economy:EconomySystem):
        self.bot = bot
        self.economy = economy

    @commands.command('create_account')
    async def create_account(self, ctx:discord.ext.commands.Context):
        """Creates a new account."""
        try:
            self.economy.create_account(ctx.author.id)
            await ctx.channel.send('Założyłem Ci konto :)')
        except:
            await ctx.channel.send('Masz już konto!')

    @commands.command('account')
    async def account(self, ctx:discord.ext.commands.Context):
        """Show user's account information."""
        money = self.economy.info(ctx.author.id)
        if money is not None:
            await ctx.channel.send(f'Masz na koncie: {money}')
        else:
            await ctx.channel.send('Obawiam się, że nie masz konta w naszym banku!')

    @commands.command('earn')
    async def earn(self, ctx:discord.ext.commands.Context, val):
        """Show user's account information."""
        if self.economy.earn(ctx.author.id, val):
            await self.account(ctx)
        else:
            await ctx.channel.send('Ewidentnie zrobiłeś coś źle.')


