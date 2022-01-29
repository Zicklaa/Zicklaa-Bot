import asyncio
import logging
import time
from datetime import datetime
from discord import message

from discord.ext import commands
import discord
from discord.raw_models import RawReactionActionEvent

logger = logging.getLogger("ZicklaaBot.Ofen")


class Reminder:
    def __init__(
        self, message_id, channel_id, user_id, text, time, id=None, parent_id=None
    ):
        self.message_id = message_id
        self.channel_id = channel_id
        self.user_id = user_id
        self.text = text
        self.time = time
        self._id = id
        self._parent_id = parent_id


class Ofen(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.cursor = db.cursor()

    @commands.command()
    async def ofen(self, ctx):
        try:
            print(ctx.author.id)
            message = ctx.message
            if int(ctx.author.id) == int(134574105109331968):
                reason = "BEI GOTT MARIAM, dein Essen verbrennt!"
                reminder_time = round(
                    time.time() + (10*60), 2
                )
                reminder = Reminder(
                    message.id, ctx.channel.id, ctx.author.id, reason, reminder_time
                )
                reminder = self.insert_reminder(reminder)
                await message.add_reaction("\N{THUMBS UP SIGN}")
                return
            else:
                await message.reply("Sorry Kiddo, Mariam only.")
        except Exception as e:
            await ctx.message.reply("Klappt nit lol 🤷")
            logger.error("Ofen Fehler: " + e)

    def insert_reminder(self, reminder: Reminder):
        try:
            sql = "INSERT INTO reminders (user_id, reminder_text, reminder_time, channel, message_id, parent_id) VALUES (?, ?, ?, ?, ?, ?)"
            val = (
                reminder.user_id,
                reminder.text,
                reminder.time,
                reminder.channel_id,
                reminder.message_id,
                reminder._parent_id,
            )
            self.cursor.execute(sql, val)
            self.db.commit()
            self.cursor.execute(
                "SELECT id FROM reminders WHERE user_id=? AND reminder_text=? AND reminder_time=? AND message_id=?",
                (reminder.user_id, reminder.text,
                 reminder.time, reminder.message_id),
            )
            id = self.cursor.fetchall()[0][0]
            logger.info("Neuer Reminder in die DB gepusht: " + str(id))
            reminder._id = id
            return reminder
        except Exception as e:
            logger.error("Remindme Fehler insert_reminder(): " + e)


def setup(bot):
    bot.add_cog(Ofen(bot, bot.db))
