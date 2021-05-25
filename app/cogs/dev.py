import psutil
from discord.ext import commands


class Dev(commands.Cog):
    """ Admin & Test features """
    hidden: bool = False

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="panel",
        aliases=('pan',),
        brief="Some data about the panel"
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def panel_stats(self, ctx):
        cols: tuple = ("blue", "green", "yellow", "orange", "red")
        mb: int = 1024 ** 2

        _embed = self.client.embed(title='Bot Stats')

        vm = psutil.virtual_memory()
        percent: int = 100 * (vm.used / vm.total)
        _embed.add_field(
            name=f":{cols[int(percent // 20)]}_square: __RAM__",
            value='\n'.join((
                f"> `{percent:.3f}` **%**",
                f" - `{vm.total / mb:,.3f}` **Mb**"
            ))
        )

        cpu_freq, cpu_percent = psutil.cpu_freq(), psutil.cpu_percent()
        _embed.add_field(
            name=f":{cols[int(cpu_percent // 20)]}_square: __CPU__",
            value='\n'.join((
                f"> `{cpu_percent:.3f}`**%**",
                f"- `{cpu_freq.current / 1000:.1f}`/`{cpu_freq.max / 1000:.1f}` **Ghz**"
            ))
        )

        disk = psutil.disk_usage('.')
        percent: int = 100 * (disk.used / disk.total)
        _embed.add_field(
            name=f":{cols[int(percent // 20)]}_square: __DISK__",
            value='\n'.join((
                f"> `{percent:.3f}` **%**",
                f"- `{disk.total / mb:,.3f}` **Mb**"
            ))
        )

        await ctx.send(embed=_embed)


def setup(client):
    client.add_cog(Dev(client))
