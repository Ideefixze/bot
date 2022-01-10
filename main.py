import discord
import secret
from discord.ext import commands

from cogs.hello import Greetings

bot = commands.Bot(command_prefix="=")
bot.add_cog(Greetings(bot))

bot.run(secret.TOKEN)