import sys

from discord.ext import commands
import discord
import asyncio


BUTTONS = {
    "prev": '⬅️',
    "next": '➡',
    "stop": '⏹',
}


async def init_buttons(msg: discord.Message):
    try:
        for reaction in BUTTONS.values():
            await msg.add_reaction(reaction)
    except Exception as e:
        print(e, file=sys.stderr)


async def clear_buttons(msg: discord.Message):
    try:
        for reaction in BUTTONS.values():
            await msg.clear_reaction(reaction)
    except Exception as e:
        print(e, file=sys.stderr)


class Paginator:
    """
    Class responsible for creating interactive message "pages".
    Users can control the displayed page by pressing reaction buttons.
    """

    def __init__(self, ctx: discord.ext.commands.Context, pages: list[...], start=0, timeout=10, loop=None):
        if len(pages) == 0:
            raise ValueError("Passed empty list to Paginator")
        self._ctx, self._pages, self._start, self._timeout = ctx, pages, start, timeout
        self._current_page = start if start < len(pages) else 0
        self._loop = loop or ctx.bot.loop

    async def _handle_message(self):
        msg = await self._ctx.send(self._pages[self._current_page])
        await init_buttons(msg)

        def check(_reaction: discord.Reaction, _user: discord.User):
            return (
                    _reaction.message.id == msg.id and
                    _user == self._ctx.message.author and
                    str(_reaction.emoji) in BUTTONS.values()
            )

        while True:
            try:
                reaction, user = await self._ctx.bot.wait_for('reaction_add', timeout=self._timeout, check=check)

                if reaction.emoji == BUTTONS["prev"]:
                    if self._current_page == 0:
                        self._current_page = len(self._pages)
                    self._current_page = self._current_page - 1
                    await msg.remove_reaction(BUTTONS["prev"], user)

                elif reaction.emoji == BUTTONS["next"]:
                    self._current_page = (self._current_page + 1) % len(self._pages)
                    await msg.remove_reaction(BUTTONS["next"], user)

                elif reaction.emoji == BUTTONS["stop"]:
                    return await clear_buttons(msg)

                await msg.edit(content=self._pages[self._current_page])

            except asyncio.TimeoutError:
                return await clear_buttons(msg)

    def create_task(self):
        """Create task in the event loop"""
        self._loop.create_task(self._handle_message())
