import asyncio
import discord
import random
import re
from .MessageProcessor import *

random.seed()

class ChannelStats(MessageProcessor):
    def __init__(self, channel):
        if channel.type is not discord.ChannelType.text:
            raise TypeError(f"Can't gather statistics for channel of type {channel.type}")
        self.channel = channel
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

        chance_diff = 0
        for embed in message.embeds:
            chance_diff +=                                                                                \
                GIF_WARNING_CHANCE_INCREMENT if embed.type == 'gifv' or (embed.type == 'image' and self.gif_regex.search(embed.url)) \
                else -GIF_WARNING_CHANCE_DECREMENT
        
        for file in message.attachments:
            chance_diff += GIF_WARNING_CHANCE_INCREMENT if file.content_type == 'image/gif' else -GIF_WARNING_CHANCE_DECREMENT
        
        #Check for GIF URLs only if we haven't detected any in embeds and attachments
        if chance_diff == 0:
            for msg_part in message.content.split():
                if (msg_part.startswith('https://') or msg_part.startswith('http://')) and self.gif_regex.search(msg_part):
                    chance_diff += GIF_WARNING_CHANCE_INCREMENT
        
        self.gif_warning_chance += chance_diff if chance_diff > 0 else -GIF_WARNING_CHANCE_DECREMENT
        if self.gif_warning_chance < 0:
            self.gif_warning_chance = 0
        elif self.gif_warning_chance > random.randrange(15, 100): #todo: decide on some constant values
            self.replies_queue.append(asyncio.create_task(message.channel.send(":anger: Nie za dużo tych GIFów?")))
            self.gif_warning_chance /= 2
