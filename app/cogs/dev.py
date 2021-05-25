from os import listdir
from typing import TYPE_CHECKING

import psutil
from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import Bot


class Dev(commands.Cog):
    """Admin & Test features"""

    def __init__(self, bot: "Bot"):
        self.bot = bot

        self.files = {}

        folders = (".", "app", "app/cogs")
        for file, path in {
            _f: path
            for path in folders
            for _f in listdir(path)
            if _f.endswith(".py")
        }.items():
            with open(f"{path}/{file}", encoding="utf-8") as f:
                self.files[file] = f.read()

        self.files["Total"] = "\n".join(self.files.values())

    @commands.command(
        name="code",
        help="Provide the code info",
    )
    @commands.is_owner()
    async def get_code(self, ctx):
        code_embed = self.bot.embed(
            title="Code Structure",
            description=(
                f"This is the whole code structure of {self.bot.user.name}!"
            ),
        )

        items = ("characters", "lines")
        for file_name, file in self.files.items():
            code_embed.add_field(
                name=f"> {file_name}",
                value="\n".join(
                    f"- `{len(f):,}` {t}"
                    for f, t in zip((file, file.splitlines()), items)
                ),
            )

        await ctx.send(embed=code_embed)

    @commands.command(
        name="panel", aliases=("pan",), help="Some data about the panel"
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.is_owner()
    async def panel_stats(self, ctx):
        cols: tuple = ("blue", "green", "yellow", "orange", "red")
        mb: int = 1024 ** 2

        _embed = self.bot.embed(title="Bot Stats")

        vm = psutil.virtual_memory()
        percent: int = 100 * (vm.used / vm.total)
        _embed.add_field(
            name=f":{cols[int(percent // 20)]}_square: __RAM__",
            value="\n".join(
                (
                    f"> `{percent:.3f}` **%**",
                    f" - `{vm.total / mb:,.3f}` **Mb**",
                )
            ),
        )

        cpu_freq, cpu_percent = psutil.cpu_freq(), psutil.cpu_percent()
        _embed.add_field(
            name=f":{cols[int(cpu_percent // 20)]}_square: __CPU__",
            value=(
                f"> `{cpu_percent:.3f}`**%**\n"
                f"- `{cpu_freq.current / 1000:.1f}`/"
                f"`{cpu_freq.max / 1000:.1f}`"
                " **Ghz**"
            ),
        )

        disk = psutil.disk_usage(".")
        percent: int = 100 * (disk.used / disk.total)
        _embed.add_field(
            name=f":{cols[int(percent // 20)]}_square: __DISK__",
            value="\n".join(
                (
                    f"> `{percent:.3f}` **%**",
                    f"- `{disk.total / mb:,.3f}` **Mb**",
                )
            ),
        )

        await ctx.send(embed=_embed)


def setup(bot: "Bot"):
    bot.add_cog(Dev(bot))
