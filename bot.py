from discord.ext import commands
from dotenv import dotenv_values

from cogs.hello import Greetings


bot = commands.Bot(command_prefix="=")
bot.add_cog(Greetings(bot))


config = dotenv_values(".env")
bot.run(config["TOKEN"])
