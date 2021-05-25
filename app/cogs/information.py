from typing import TYPE_CHECKING

import discord
from discord.ext import commands


if TYPE_CHECKING:
    from app.bot import Bot


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='help',
        aliases=('all', 'all_cmds', 'cmds'),
        brief="List every command osf the bot"
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def all_commands(self, ctx):
        """ Provide a list of every command available command for the user,
        split by extensions and organized in alphabetical order.
        Will not show the event-only extensions """

        help_embed = discord.Embed(
            title='All commands',
            description=f"> `{len(self.bot.commands)}` commands available"
        )

        for cog_name, cog in self.bot.cogs.items():
            if len(cog.get_commands()):
                help_embed.add_field(
                    name=cog_name.capitalize(),
                    value='  •  '.join(sorted(f'`{c.name}`' for c in cog.get_commands())),
                    inline=False
                )

        await ctx.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Information(bot))
