import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

INTENTS = discord.Intents.default()
INTENTS.members = True


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=INTENTS,
        )

        for filename in os.listdir("cogs"):
            if filename.endswith('py'):
                self.load_extension(f"cogs.{filename[:-3]}")
                print('-', filename)

    def run(self):
        return super().run(os.getenv("TOKEN"))

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        await ctx.send(repr(error))

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.guild:
            return

        if message.guild.id != self.get_cog("DonorRole").mcoding_server_id:
            return

        await self.process_commands(message)

    async def on_ready(self):
        print(f"Logged in as {self.user}!")
