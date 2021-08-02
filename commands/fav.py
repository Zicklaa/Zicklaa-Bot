import logging

from collections.abc import Sequence
import discord
import datetime
from pytz import timezone
from discord.ext import commands
from discord.raw_models import RawReactionActionEvent

logger = logging.getLogger("ZicklaaBot.Fav")




class Fav(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.cursor = db.cursor()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        message_id, channel_id, emoji, user_id = self.parse_raw_reaction_event(payload)
        if str(emoji) == "🦶":
            try:
                user = await self.bot.fetch_user(payload.user_id)
                dm_channel = await user.create_dm()
                await dm_channel.send("Antworte bitte mit dem gewünschten Namen für den Fav.")
                response = await self.bot.wait_for('message', check=message_check(channel=dm_channel))
                name = response.content
                if len(name)<250:
                    sql = "INSERT INTO favs (user_id, message_id, name, channel_id) VALUES (?, ?, ?, ?)"
                    val = (
                        user_id,
                        message_id,
                        name,
                        channel_id,
                    )
                    self.cursor.execute(sql, val)
                    self.db.commit()
                    await response.add_reaction("\N{THUMBS UP SIGN}")
                    logger.info("Neuer Fav angelegt für für: " + response.author.name)
                else:
                    await response.reply("Zu lang. Bidde unter 250chars")
                    response = await self.bot.wait_for('message', check=message_check(channel=dm_channel))
                    name = response.content
                    if len(name)<250:
                        sql = "INSERT INTO favs (user_id, message_id, name, channel_id) VALUES (?, ?, ?, ?)"
                        val = (
                            user_id,
                            message_id,
                            name,
                            channel_id,
                        )
                        self.cursor.execute(sql, val)
                        self.db.commit()
                        await response.add_reaction("\N{THUMBS UP SIGN}")
                        logger.info("Neuer Fav angelegt für für: " + response.author.name)
                    else:
                        await response.reply("Dummkopf")
            except Exception as e:
                await response.reply("Klappt nit lol 🤷")
                logger.error(f"Lustiges Bilchen ERROR von {response.author.name}: {e}")
    

    @commands.command()
    async def fav(self, ctx, *name):
        #try:
        name = " ".join(name)
        if name:
            fav = self.cursor.execute(
            "SELECT * FROM favs WHERE name=? AND user_id=?", (name, ctx.author.id,)
            ).fetchone()
            if fav:
                try:
                    channel = self.bot.get_channel(fav[4])
                    fav_message = await channel.fetch_message(fav[2])
                    embed = discord.Embed(title="", description=fav_message.content, color=0x00ff00)
                    current_time = (fav_message.created_at + datetime.timedelta(hours=2)).strftime("%d.%m.%Y, %H:%M:%S")
                    if fav_message.attachments:
                        embed.set_image(url=str(fav_message.attachments[0].url))
                    embed.set_author(name=fav_message.author.name, icon_url=fav_message.author.avatar_url)
                    embed.set_footer(text=current_time + ' | #' + fav_message.channel.name + " | by: " + ctx.author.name)
                    await ctx.channel.send(embed=embed)
                    await ctx.message.delete()
                except Exception as e:
                    await ctx.message.reply("Klappt nit lol 🤷")
                    logger.error(f"Fav ERROR von {ctx.author.name}: {e}")
            else:
                await ctx.message.add_reaction("\N{NO ENTRY SIGN}")
                await ctx.message.add_reaction("\N{LEFT-POINTING MAGNIFYING GLASS}")
        else:
            fav = self.cursor.execute(
            "SELECT * FROM favs WHERE user_id=? ORDER BY RANDOM()", (ctx.author.id,)
            ).fetchone()
            if fav:
                try:
                    channel = self.bot.get_channel(fav[4])
                    fav_message = await channel.fetch_message(fav[2])
                    embed = discord.Embed(title="", description=fav_message.content, color=0x00ff00)
                    current_time = (fav_message.created_at + datetime.timedelta(hours=2)).strftime("%d.%m.%Y, %H:%M:%S")
                    if fav_message.attachments:
                        embed.set_image(url=str(fav_message.attachments[0].url))
                    embed.set_author(name=fav_message.author.name, icon_url=fav_message.author.avatar_url)
                    embed.set_footer(text=current_time + ' | #' + fav_message.channel.name + " | by: " + ctx.author.name)
                    await ctx.channel.send(embed=embed)
                    await ctx.message.delete()
                except Exception as e:
                    await ctx.message.reply("Klappt nit lol 🤷")
                    logger.error(f"Fav ERROR von {ctx.author.name}: {e}")

    def parse_raw_reaction_event(self, payload: RawReactionActionEvent):

        return payload.message_id, payload.channel_id, payload.emoji, payload.user_id

def setup(bot):
    bot.add_cog(Fav(bot, bot.db))

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
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