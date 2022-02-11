import discord
from discord.ext import commands

from .DatabaseHandler import DatabaseHandler
from .Account import Account


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = DatabaseHandler().session

    @commands.command('create_account')
    async def create_account(self, ctx:discord.ext.commands.Context):
        """Creates a new account."""
        self.session.add(Account(id=ctx.author.id, money=1.0))
        self.session.commit()
        await ctx.channel.send('Account created.')

    @commands.command('account')
    async def account(self, ctx:discord.ext.commands.Context):
        """Show user's account information."""
        try:
            account = self.session.query(Account).get(ctx.author.id)
            await ctx.channel.send(f'You have: {account.money}')
        except:
            await ctx.channel.send(f'Please, make an account first.')


