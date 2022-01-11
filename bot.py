import secret
from discord.ext import commands

from cogs.hello import Greetings
from cogs.periodic.waifu import Waifu

bot = commands.Bot(command_prefix="=")
bot.add_cog(Greetings(bot))
bot.add_cog(Waifu(bot))

bot.run(secret.TOKEN)


