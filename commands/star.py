import logging
import discord
from discord.ext import commands
from discord.raw_models import RawReactionActionEvent
from collections.abc import Sequence
from dateutil import tz
import pytz

logger = logging.getLogger("ZicklaaBot.Star")

post_channel_id = 981543834129428560  # Mainchannel
# post_channel_id = 567411189336768532  # Testchannel
threshold = 5
ext_list = [
    "3g2",
    "3gp",
    "amv",
    "asf",
    "avi",
    "gifv",
    "m4p",
    "m4v",
    "mov",
    "mp2",
    "mp4",
    "mpeg",
    "mpg",
    "webm",
]
path = "/home/zicklaa/Zicklaa-Bot/LustigeBildchen/"


class Star(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.cursor = db.cursor()

    def parse_raw_reaction_event(self, payload: RawReactionActionEvent):
        return payload.message_id, payload.channel_id, payload.emoji, payload.user_id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        message_id, channel_id, emoji, user_id = self.parse_raw_reaction_event(payload)
        if str(emoji) == "⭐" and int(channel_id) != post_channel_id:
            # try:
            cache_msg = discord.utils.get(self.bot.cached_messages, id=message_id)
            reactions = cache_msg.reactions
            star_dict = {}
            for reaction in reactions:
                star_dict.update({reaction.emoji: reaction.count})
            if int(star_dict["⭐"]) == threshold:
                try:
                    self.cursor.row_factory = lambda cursor, row: row[0]
                    posted_stars = self.cursor.execute(
                        "SELECT message_id FROM stars"
                    ).fetchall()
                except Exception as e:
                    logger.error(f"Noch keine geposteten Stars: {e}")
                if message_id not in posted_stars:
                    channel = self.bot.get_channel(channel_id)
                    message = await channel.fetch_message(message_id)
                    embed = discord.Embed(
                        title="", description=message.content, color=0xFFEA00
                    )
                    time = (
                        pytz.utc.localize(message.created_at).astimezone(tz.tzlocal())
                    ).strftime("%d.%m.%Y, %H:%M:%S")
                    if message.attachments:
                        if any(ext in message.attachments[0].url for ext in ext_list):
                            embed.add_field(
                                name="Link zum Video:",
                                value="[Video](" + message.attachments[0].url + ")",
                                inline=True,
                            )
                        else:
                            embed.set_image(url=str(message.attachments[0].url))
                            try:
                                for i, attachements in enumerate(message.attachments):
                                    filename = (
                                        path
                                        + "STERNBRETT_"
                                        + str(message_id)
                                        + "_"
                                        + str(i)
                                        + ".png"
                                    )
                                    await attachements.save(filename)
                            except:
                                logger.error(f"Star Error beim LTB speichern: {e}")

                    embed.add_field(
                        name="Link zur Nachricht:",
                        value="[Nachricht](" + message.jump_url + ")",
                        inline=True,
                    )
                    embed.set_author(
                        name=message.author.name,
                        icon_url=message.author.avatar_url,
                        url=message.jump_url,
                    )
                    embed.set_footer(text=time + " | #" + message.channel.name)
                    channel = self.bot.get_channel(post_channel_id)
                    star_message = await channel.send(embed=embed)
                    await star_message.add_reaction("⭐")
                    try:
                        sql = "INSERT INTO stars (message_id) VALUES (?)"
                        val = (int(message_id),)
                        self.cursor.execute(sql, val)
                        self.db.commit()
                    except Exception as e:
                        logger.error(f"Star Error beim DB pushen: {e}")

                    logger.info("Star gepostet")
            """except Exception as e:
                logger.error(f"Star Error: {e}")"""

    @commands.command()
    async def star(self, ctx, link):
        try:
            if int(ctx.author.id) == 288413759117066241:
                if link:
                    try:
                        link = link.split("/")
                        channel_id = int(link[5])
                        msg_id = int(link[6])
                        channel = self.bot.get_channel(channel_id)
                        message = await channel.fetch_message(msg_id)
                        try:
                            self.cursor.row_factory = lambda cursor, row: row[0]
                            posted_stars = self.cursor.execute(
                                "SELECT message_id FROM stars"
                            ).fetchall()
                        except Exception as e:
                            logger.error(f"Noch keine geposteten Stars: {e}")
                        if msg_id not in posted_stars:
                            channel = self.bot.get_channel(channel_id)
                            message = await channel.fetch_message(msg_id)
                            embed = discord.Embed(
                                title="", description=message.content, color=0xFFEA00
                            )
                            time = (
                                pytz.utc.localize(message.created_at).astimezone(
                                    tz.tzlocal()
                                )
                            ).strftime("%d.%m.%Y, %H:%M:%S")
                            if message.attachments:
                                if any(
                                    ext in message.attachments[0].url
                                    for ext in ext_list
                                ):
                                    embed.add_field(
                                        name="Link zum Video:",
                                        value="[Video]("
                                        + message.attachments[0].url
                                        + ")",
                                        inline=True,
                                    )
                                else:
                                    embed.set_image(url=str(message.attachments[0].url))
                            embed.add_field(
                                name="Link zur Nachricht:",
                                value="[Nachricht](" + message.jump_url + ")",
                                inline=True,
                            )
                            embed.set_author(
                                name=message.author.name,
                                icon_url=message.author.avatar_url,
                                url=message.jump_url,
                            )
                            embed.set_footer(text=time + " | #" + message.channel.name)
                            channel = self.bot.get_channel(post_channel_id)
                            star_message = await channel.send(embed=embed)
                            await star_message.add_reaction("⭐")
                            await ctx.add_reaction("✅")
                            try:
                                sql = "INSERT INTO stars (message_id) VALUES (?)"
                                val = (int(msg_id),)
                                self.cursor.execute(sql, val)
                                self.db.commit()
                            except Exception as e:
                                await ctx.add_reaction("❌")
                                logger.error(f"Star Error beim DB pushen: {e}")

                            logger.info("Star gepostet")
                    except Exception as e:
                        await ctx.reply("Link br0ke 🤷")
                        await ctx.add_reaction("❌")
                        logger.error(f"Star from {ctx.author.name}: {e}")
                else:
                    await ctx.reply(
                        "Wie soll ich das sternen wenn du nichtmal ne Link gibst, du Mong?"
                    )
                    await ctx.add_reaction("❌")
                    logger.info("Star(): Kein Link gegeben von: " + ctx.author.name)
            else:
                await ctx.add_reaction("❌")
                await ctx.reply("Das ist VERBOTEN!!")
                logger.info("Star(): Kein Admin von: " + ctx.author.name)
        except Exception as e:
            await ctx.add_reaction("❌")
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Star from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Star(bot, bot.db))


def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)


def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    try:
        channel = make_sequence(channel)
        author = make_sequence(author)
        content = make_sequence(content)
        if lower:
            content = tuple(c.lower() for c in content)

        def check(message):
            if ignore_bot and message.author.bot:
                return False
            if channel and message.channel not in channel:
                return False
            if author and message.author not in author:
                return False
            actual_content = message.content.lower() if lower else message.content
            if content and actual_content not in content:
                return False
            return True

        return check
    except Exception as e:
        logger.error(e)
