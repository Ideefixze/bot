import asyncio
import discord
import secret
import random
import re

from discord.ext import commands
from cogs.hello import Greetings
from MessageProcessor import *

class ChannelStats(MessageProcessor):
    def __init__(self, channel):
        self.channel = channel #todo: assert text channel (has name etc)
        self.replies_queue = []

        #GIF checker processor
        self.gif_regex = re.compile('\.gif\?*\S*$')
        self.gif_warning_chance = 0
    
    def process(self, message):
        if message.channel.id != self.channel.id:
            raise ValueError('Message to be processed does not come from channel {} - src channel ID: {}, src channel type: {}'
                                .format(self.channel.name, message.channel.id, message.channel.type))
        super().process(message)
    
    async def send_replies(self):
        for reply in self.replies_queue:
            await reply
        self.replies_queue.clear()
    
    @processor
    def check_for_gif(self, message):
        GIF_WARNING_CHANCE_INCREMENT = 5
        GIF_WARNING_CHANCE_DECREMENT = 1

        previous_chance = self.gif_warning_chance
        def report_embed(is_gif):
            diff = GIF_WARNING_CHANCE_INCREMENT if is_gif else -GIF_WARNING_CHANCE_DECREMENT
            self.gif_warning_chance += diff
            if self.gif_warning_chance < 0:
                self.gif_warning_chance = 0
        
        for embed in message.embeds:
            if embed.type == 'gifv' or (embed.type == 'image' and self.gif_regex.search(embed.url)):
                report_embed(True)
            else:
                report_embed(False)
        
        for file in message.attachments:
            if file.content_type == 'image/gif':
                report_embed(True)
            else:
                report_embed(False)
        
        #Check for GIF URLs only if we haven't detected any in embeds and attachments
        if previous_chance == self.gif_warning_chance:
            for msg_part in message.content.split():
                if (msg_part.startswith('https://') or msg_part.startswith('http://')) and self.gif_regex.search(msg_part):
                    report_embed(True)
        
        if previous_chance == self.gif_warning_chance:
            self.gif_warning_chance -= GIF_WARNING_CHANCE_DECREMENT
            if self.gif_warning_chance < 0:
                self.gif_warning_chance = 0
        
        elif self.gif_warning_chance > random.randrange(15, 100): #todo: decide on some constant values
            self.replies_queue.append(asyncio.create_task(message.channel.send(":anger: Nie za dużo tych GIFów?")))
            self.gif_warning_chance /= 2



random.seed()
bot = commands.Bot(command_prefix="=")
bot.add_cog(Greetings(bot))
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
