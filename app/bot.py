import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

EXTENSIONS = [
    "app.cogs.donor_role"
]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

        for ext in EXTENSIONS:
            self.load_extension(ext)

    def run(self):
        return super().run(os.getenv("TOKEN"))

    async def on_command_error(self, ctx: commands.Context, err: Exception):
        await ctx.send(err)

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
