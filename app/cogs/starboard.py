from sqlite3.dbapi2 import IntegrityError, Row
from typing import List, Optional, TYPE_CHECKING, Tuple, Union

import discord
from discord.ext import commands

from app.constants import MISSING, ZWS

if TYPE_CHECKING:
    from app.bot import Bot


def plain_text(message: discord.Message, points: int) -> str:
    return f":star: **{points}** | {message.channel.mention}"


async def embed_message(
    bot: "Bot", message: discord.Message, files: bool = True
) -> Tuple[discord.Embed, List[discord.File]]:
    nsfw = message.channel.is_nsfw()
    content = message.system_content

    urls = []
    extra_attachments = []
    image_used = False
    thumbnail_used = False

    for attachment in message.attachments:
        if files:
            try:
                f = await attachment.to_file()
            except (discord.Forbidden, discord.HTTPException):
                f = None
        else:
            f = None
        urls.append(
            {
                "name": attachment.filename,
                "display_url": attachment.url,
                "url": attachment.url,
                "type": "upload",
                "spoiler": attachment.is_spoiler(),
                "file": f,
                "show_link": True,
                "thumbnail_only": False,
            }
        )

    embed: discord.Embed
    for embed in message.embeds:
        if embed.type in ["rich", "article", "link"]:
            if embed.title != embed.Empty:
                if embed.url == embed.Empty:
                    content += f"\n\n__**{embed.title}**__\n"
                else:
                    content += f"\n\n__**[{embed.title}]({embed.url})**__\n"
            else:
                content += "\n"
            content += (
                (f"{embed.description}\n")
                if embed.description != embed.Empty
                else ""
            )

            for field in embed.fields:
                name = f"\n**{field.name}**\n"
                value = f"{field.value}\n"

                content += name + value
            if embed.footer.text is not embed.Empty:
                content += f"{embed.footer.text}"
            if embed.image.url is not embed.Empty:
                urls.append(
                    {
                        "name": "Embed Image",
                        "url": embed.image.url,
                        "display_url": embed.image.url,
                        "type": "image",
                        "spoiler": False,
                        "show_link": False,
                        "thumbnail_only": False,
                    }
                )
            if embed.thumbnail.url is not embed.Empty:
                urls.append(
                    {
                        "name": "Embed Thumbnail",
                        "url": embed.thumbnail.url,
                        "display_url": embed.thumbnail.url,
                        "type": "image",
                        "spoiler": False,
                        "show_link": False,
                        "thumbnail_only": True,
                    }
                )

        elif embed.url is not embed.Empty:
            new_url = {
                "display_url": embed.thumbnail.url,
                "url": embed.url,
                "type": "gif" if embed.type == "gifv" else embed.type,
                "spoiler": False,
                "show_link": True,
                "thumbnail_only": False
            }
            if embed.type == "image":
                new_url = {"name": "Image", **new_url}
            elif embed.type == "gifv":
                new_url = {"name": "GIF", **new_url}
            elif embed.type == "video":
                new_url = {"name": embed.title, **new_url}

            urls.append(new_url)

    if len(content) > 6_000:
        to_remove = len(content + " ...") - 6_000
        content = content[:-to_remove]

    _a = message.author
    author_name = (f"{_a.display_name}#{_a.discriminator}")

    embed = discord.Embed(
        color=bot.theme,
        description=content,
    ).set_author(name=author_name, icon_url=message.author.avatar_url)

    ref_message = None
    ref_jump = None
    ref_author = None
    if message.reference is not None and bot.get_guild(
        message.reference.guild_id
    ):
        if message.reference.resolved is None:
            ref_message = await bot.fetch_message(
                bot.get_channel(message.reference.channel_id),
                message.reference.message_id
            )
            if ref_message is None:
                ref_content = "*Message was deleted*"
            else:
                ref_author = str(ref_message.author)
                ref_content = ref_message.system_content
        else:
            ref_message = message.reference.resolved
            if isinstance(message.reference.resolved, discord.Message):
                ref_content = message.reference.resolved.system_content
                ref_author = str(ref_message.author)
            else:
                ref_content = "*Message was deleted*"

        if ref_content == "":
            ref_content = "*File Only*"

        embed.add_field(
            name=f'Replying to {ref_author or "Unknown"}',
            value=ref_content,
            inline=False,
        )

        if isinstance(ref_message, discord.Message):
            ref_jump = "**[Replying to {0}]({1})**\n".format(
                ref_author, ref_message.jump_url
            )
        else:
            ref_jump = (
                "**[Replying to Unknown (deleted)]"
                "(https://discord.com/channels/{0.guild_id}/"
                "{0.channel_id}/{0.message_id})**\n"
            ).format(message.reference)

    embed.add_field(
        name=ZWS,
        value=str(
            str(ref_jump if ref_message else "")
            + "**[Jump to Message]({0})**".format(message.jump_url),
        ),
        inline=False,
    )

    image_types = ["png", "jpg", "jpeg", "gif", "gifv", "svg", "webp"]
    for data in urls:
        if data["type"] == "upload":
            is_image = False
            for t in image_types:
                if data["url"].endswith(t):
                    is_image = True
                    break
            added = False
            if is_image and not nsfw and not data["spoiler"]:
                if not image_used:
                    embed.set_image(url=data["display_url"])
                    image_used = True
                    added = True
            if not added and data["file"] is not None:
                f: discord.File = data["file"]
                if nsfw:
                    f.filename = "SPOILER_" + f.filename
                extra_attachments.append(f)
        elif not nsfw:
            if data["thumbnail_only"]:
                if not thumbnail_used:
                    embed.set_thumbnail(url=data["display_url"])
                    thumbnail_used = True
            elif not image_used:
                embed.set_image(url=data["display_url"])
                image_used = True

    to_show = str(
        "\n".join(
            f"**[{d['name']}]({d['url']})**" for d in urls if d["show_link"]
        )
    )

    if len(to_show) != 0:
        embed.add_field(name=ZWS, value=to_show)

    embed.timestamp = message.created_at

    return embed, extra_attachments


async def original_message(bot: "Bot", message_id: int) -> Optional[Row]:
    from_id = await bot.db.fetchone(
        """SELECT * FROM messages
        WHERE id=?""",
        (message_id,)
    )
    if from_id:
        return from_id

    from_starboard_id = await bot.db.fetchone(
        """SELECT * FROM messages
        WHERE starboard_message_id=?""",
        (message_id,)
    )
    if from_starboard_id:
        return from_starboard_id

    return None


async def update_message(
    bot: "Bot",
    channel: Union[discord.TextChannel, int],
    orig_message: Union[discord.Message, int],
    starboard_message: Union[
        discord.Message, int, None
    ] = MISSING,
):
    if isinstance(channel, int):
        channel = bot.get_channel(channel)
    if isinstance(orig_message, int):
        orig_message = await bot.fetch_message(channel, orig_message)

    starboard = bot.starboard_channel
    if isinstance(starboard_message, int):
        starboard_message = await bot.fetch_message(
            starboard,
            starboard_message
        )
    elif starboard_message is MISSING:
        sql_orig = await bot.db.fetchone(
            """SELECT * FROM messages
            WHERE id=?""",
            (orig_message.id,)
        )
        if sql_orig and sql_orig["starboard_message_id"]:
            starboard_message = await bot.fetch_message(
                starboard,
                int(sql_orig["starboard_message_id"])
            )
        else:
            starboard_message = None

    points = (await bot.db.fetchone(
        """SELECT COUNT(*) FROM stars
        WHERE message_id=?""",
        (orig_message.id,)
    ))["COUNT(*)"]

    if starboard_message:
        embed, _ = await embed_message(
            bot, orig_message, False
        )
        await starboard_message.edit(
            content=plain_text(orig_message, points),
            embed=embed
        )
    else:
        if points >= bot.config.starboard_limit:
            embed, files = await embed_message(
                bot, orig_message
            )
            msg: discord.Message = await starboard.send(
                plain_text(orig_message, points),
                embed=embed,
                files=files
            )
            await bot.db.execute(
                """UPDATE MESSAGES
                SET starboard_message_id=?
                WHERE id=?""",
                (msg.id, orig_message.id,)
            )
            await msg.add_reaction("⭐")


class StarboardEvents(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @property
    def starboard_valid(self) -> bool:
        return self.bot.starboard_channel is not None

    def is_payload_valid(
        self, payload: discord.RawReactionActionEvent
    ) -> bool:
        if payload.guild_id != self.bot.mcoding_server.id:
            return False
        if not self.starboard_valid:
            return False
        if payload.member and payload.member.bot:
            return False
        if payload.emoji.name != "⭐":
            return False
        return True

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self, payload: discord.RawReactionActionEvent
    ):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()
        if not self.is_payload_valid(payload):
            return

        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return

        # TODO: cache messages
        try:
            act_message: discord.Message = await self.bot.fetch_message(
                channel,
                payload.message_id
            )
        except discord.NotFound:
            return

        sql_message = await original_message(self.bot, payload.message_id)
        if sql_message is None:
            await self.bot.db.execute(
                """INSERT INTO messages (id, channel_id, author_id)
                VALUES (?, ?, ?)""",
                (payload.message_id, payload.channel_id, act_message.author.id)
            )
            sql_message = await self.bot.db.fetchone(
                """SELECT * FROM messages WHERE id=?""",
                (payload.message_id,)
            )

        if int(sql_message["id"]) != act_message.id:
            channel = self.bot.get_channel(int(sql_message["channel_id"]))
            try:
                message = await self.bot.fetch_message(
                    channel, int(sql_message["id"])
                )
            except discord.NotFound:
                return
        else:
            message = act_message

        if message.author.id == payload.user_id:
            # Remove self stars
            await act_message.remove_reaction(payload.emoji, payload.member)
            return

        try:
            await self.bot.db.execute(
                """INSERT INTO stars (message_id, user_id)
                VALUES (?, ?)""",
                (message.id, payload.user_id,)
            )
        except IntegrityError:
            pass

        await update_message(
            self.bot,
            channel,
            message,
        )

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, payload: discord.RawReactionActionEvent
    ):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()
        if not self.is_payload_valid(payload):
            return

        original = await original_message(self.bot, payload.message_id)
        if not original:
            return

        await self.bot.db.execute(
            """DELETE FROM stars
            WHERE message_id=?
            AND user_id=?""",
            (original["id"], payload.user_id,)
        )

        await update_message(
            self.bot, int(original["channel_id"]), int(original["id"])
        )


def setup(bot: "Bot"):
    bot.add_cog(StarboardEvents(bot))
