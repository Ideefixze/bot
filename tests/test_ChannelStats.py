import asyncio
import discord
import pytest
from pytest_mock import MockerFixture
from types import SimpleNamespace

from bot.ChannelStats import ChannelStats


def create_mock_channel(mocker, id, type, name=''):
    send_stub = mocker.stub(name='send_stub')
    async def send(*args, **kwargs):
        send_stub(*args, **kwargs)
    send.stub = send_stub

    channel = SimpleNamespace()
    channel.id = id
    channel.type = type
    channel.name = name
    channel.send = send
    return channel

def create_mock_message(id, channel, content, attachments, embeds):
    msg = SimpleNamespace()
    msg.id = id
    msg.channel = channel
    msg.content = content
    msg.attachments = attachments
    msg.embeds = embeds
    return msg

def create_mock_attachment(content_type, url):
    file = SimpleNamespace()
    file.content_type = content_type
    file.url = url
    return file

def create_mock_embed(type, url):
    embed = SimpleNamespace()
    embed.type = type
    embed.url = url
    return embed

def test_create_ChannelStats(mocker: MockerFixture):
    guild_channel = create_mock_channel(mocker, 1, discord.ChannelType.text, 'ch')
    stats = ChannelStats(guild_channel)
    assert stats.message_processors
    assert stats.gif_warning_chance == 0
    private_channel = create_mock_channel(mocker, 2, discord.ChannelType.private)
    with pytest.raises(TypeError): stats = ChannelStats(private_channel)

def test_matching_message_and_channel(mocker: MockerFixture):
    channel = create_mock_channel(mocker, 1, discord.ChannelType.text, 'ch1')
    other_channel = create_mock_channel(mocker, 2, discord.ChannelType.text, 'ch2')
    msg = create_mock_message(1, channel, '', [], [])
    other_msg = create_mock_message(2, other_channel, '', [], [])
    stats = ChannelStats(channel)
    stats.process(msg)
    with pytest.raises(ValueError): stats.process(other_msg)

def test_gif_flood_warning(mocker: MockerFixture):
    channel = create_mock_channel(mocker, 1, discord.ChannelType.text, 'ch1')
    non_gif_messages = [
        create_mock_message(1, channel, 'lorem ipsum dolores', [], []),
        create_mock_message(2, channel, '', [], [create_mock_embed('link', 'https://cirno.pl')]),
        create_mock_message(3, channel, '', [create_mock_attachment('image/jpeg', 'https://cirno.pl/cirno.jpg')], [])
    ]
    gif_messages = [
        create_mock_message(4, channel, 'https://cirno.pl/fairy.gif', [], []),
        create_mock_message(5, channel, '', [], [create_mock_embed('gifv', 'https://cirno.pl/fairy.gif')]),
        create_mock_message(6, channel, '', [create_mock_attachment('image/gif', 'https://cirno.pl/fairy.gif')], [])
    ]

    stats = ChannelStats(channel)
    for msg in non_gif_messages:
        stats.process(msg)
        assert stats.gif_warning_chance == 0
    
    async def process_gif_messages():
        for x in range(0, 20):
            for msg in gif_messages:
                stats.process(msg)
                assert stats.gif_warning_chance > 0
        await stats.send_replies()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_gif_messages())
    channel.send.stub.assert_called()
    
    async def process_single_message(msg, is_gif_msg):
        stats.process(msg)
        assert stats.replies_queue if is_gif_msg else True
        await stats.send_replies()
    
    stats.gif_warning_chance = 9999
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_single_message(non_gif_messages[0], False))
    loop.run_until_complete(process_single_message(gif_messages[0], True))
    loop.close()
