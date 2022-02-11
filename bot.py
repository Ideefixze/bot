import discord
import secret
from discord.ext import commands

from cogs.economy.economy import Economy
from cogs.hello import Greetings
from ChannelStats import ChannelStats

bot = commands.Bot(command_prefix="=")
bot.add_cog(Greetings(bot))
bot.add_cog(Economy(bot))
channels_statistics = {}

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.type == discord.MessageType.default:
        stats = channels_statistics.setdefault(message.channel.id, ChannelStats(message.channel))
        stats.process(message)
        await stats.send_replies()

if __name__ == '__main__':
    bot.run(secret.TOKEN)
