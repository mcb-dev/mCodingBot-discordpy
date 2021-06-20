import requests
import time
from typing import TYPE_CHECKING
from discord.ext import commands, tasks

if TYPE_CHECKING:
    from app.bot import Bot

BASE_URL = "https://www.googleapis.com/youtube/v3/channels"


class YtStatistics(commands.Cog):

    def __init__(self, bot: "Bot"):
        self.bot = bot

        if self.bot.config.sub_count_channel is not None:
            self.update_sub_count.start()

        if self.bot.config.view_count_channel is not None:
            self.update_view_count.start()

        self._stat_update = 0
        self._last_stats = {'subs': '?', 'views': '?'}  # DONT REMOVE THIS !
        self._last_stats = self.channel_stats

    @property
    def channel_stats(self):
        if self._stat_update == (time.time() // 100):
            return self._last_stats

        self.bot.log("Retrieving channel stats....")

        link = f"{BASE_URL}?part=statistics&id={self.bot.config.mcoding_yt_id}&key={self.bot.config.yt_api_key}"
        response = requests.get(link).json()

        if not response:
            return self._last_stats

        items = response.get("items")
        if not items:
            return self._last_stats

        channel = items[0]
        if channel.get("id") != self.bot.config.mcoding_yt_id:
            return self._last_stats

        statistics = channel.get('statistics')
        if not statistics:
            return self._last_stats

        subs = float(statistics.get('subscriberCount', 0))
        views = float(statistics.get('viewCount', 0))

        if not subs or not views:
            return self._stat_update

        self.bot.log("Youtube statistics fetched !")
        self._last_stats = {'subs': f"{subs:,.0f}", 'views': f"{views:,.0f}"}
        self._stat_update = time.time() // 100
        return self._last_stats

    @tasks.loop(minutes=10)
    async def update_sub_count(self):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()

        await self.bot.sub_count_channel.edit(
            name=f"Subs: {self.channel_stats['subs']}"
        )

    @tasks.loop(minutes=10)
    async def update_view_count(self):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()

        await self.bot.view_count_channel.edit(
            name=f"Views: {self.channel_stats['views']}"
        )


def setup(bot: "Bot"):
    bot.add_cog(YtStatistics(bot))
