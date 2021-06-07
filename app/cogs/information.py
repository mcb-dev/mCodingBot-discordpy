from platform import python_version
from time import perf_counter
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import Bot


class Information(commands.Cog):
    """Bot information"""

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(name="links", help="Useful links.")
    async def links(self, ctx: commands.Context):
        embed = self.bot.embed(
            title="Useful Links",
            description="<useful links here>",
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="ping", aliases=("latency", "lat", "ms"), brief="Pong !"
    )
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """Get the latency of the client converted in milliseconds.
        An dynamically colored ball will show in the image in function of
        the ping. Give also worst, best and daily average ping"""
        latencies: dict = {"API": self.bot.latency}

        marker: float = perf_counter()
        ping_message = await ctx.send("> pinging...")
        latencies["BOT"] = perf_counter() - marker

        _embed = self.bot.embed(
            title=f"{ctx.author.name} Ponged !",
            description="The bot and API latency",
        )

        for k, v in latencies.items():
            _embed.add_field(
                name=f"{k} latency", value=f"> `{v * 1e3:,.2f} ms`"
            )

        await ping_message.edit(content=" ", embed=_embed)

    @commands.command(
        name="user",
        aliases=("whois", "more"),
        brief="return the user information",
    )
    async def user(self, ctx, user: discord.Member = None):
        """return the user information"""
        if user is None:
            user = ctx.author

        embed = self.bot.embed()
        embed.set_thumbnail(url=user.avatar_url)

        embed.set_author(
            name=f"{user.name}%s Information"
            % ("'" if user.name.endswith("s") else "'s"),
            icon_url=user.avatar_url,
        )

        if user.nick is not None:
            embed.add_field(name="> nickname", value=f"`{user.nick}`")

        for name, value in {
            "default avatar": user.default_avatar,
            "platform": "Mobile" if user.is_on_mobile() else "computer",
            "status": user.status,
            "discriminator": user.discriminator,
            "created date": user.created_at.strftime("%d %b. %Y"),
            "joined date": user.joined_at.strftime("%d %b. %Y"),
        }.items():
            embed.add_field(name=f"> {name}", value=f"`{value}`")

        if user.activity is not None:
            embed.add_field(name="> Activity", value=user.activity.name)

        if len(user.roles) < 50:
            roles = ", ".join([f"{role.name}" for role in user.roles[:0:-1]])
        else:
            roles = "too many roles"

        embed.add_field(
            name="> roles (%i)" % (len(user.roles) - 1),
            value=f"```c\n{roles} ```",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command(name="bot", brief="Display the bot information")
    async def info_bot(self, ctx):
        """Display the bot information"""
        _embed = self.bot.embed(
            title=f"{self.bot.user.name} Bot Information",
            description="\n".join(
                (
                    "This bot was created by Circuit#5585, Sigmanificient#330,"
                    " and trag1c#3879.",
                    self.bot.user.created_at.strftime(
                        "> **Creation date** : %A %d %B %Y at %H:%M"
                    ),
                )
            ),
        )

        for key, val in {
            "Python": python_version(),
            "Discord": discord.__version__,
            "Commands": len(self.bot.commands),
            "Extensions": len(self.bot.cogs),
        }.items():
            _embed.add_field(name=key, value=f"> `{val}`", inline=True)

        await ctx.send(embed=_embed)

    @commands.command(
        name="all",
        aliases=("all_cmds", "cmds"),
        brief="List every command osf the bot",
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def all_commands(self, ctx):
        """Provide a list of every command available command for the user,
        split by extensions and organized in alphabetical order.
        Will not show the event-only extensions"""

        _embed = self.bot.embed(
            title="All commands",
            description=f"> `{len(self.bot.commands)}` commands available",
        )

        for cog_name, cog in self.bot.cogs.items():
            if len(cog.get_commands()):
                _embed.add_field(
                    name=cog_name.capitalize(),
                    value="  •  ".join(
                        sorted(f"`{c.name}`" for c in cog.get_commands())
                    ),
                    inline=False,
                )

        await ctx.send(embed=_embed)


def setup(bot: "Bot"):
    bot.add_cog(Information(bot))
