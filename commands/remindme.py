import asyncio
import logging
import time
from datetime import datetime
from dateutil import tz
from discord.ext import commands
from utils.parser import RemindmeParser
from config import globalPfad

logger = logging.getLogger("ZicklaaBot.RemindMe")


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


def reminder_from_record(record):
    return Reminder(
        record[5], record[4], record[1], record[2], record[3], record[0], record[6]
    )


class RemindMe(commands.Cog):
    def __init__(self, bot, db, json_model):
        self.bot = bot
        self.db = db
        self.json_model = json_model
        self.cursor = db.cursor()
        self.global_state = {}
        with open(globalPfad + "utils/rm_grammar.peg", 'r') as f:
            grm = f.read()
            self.parser = RemindmeParser(grm)

    @commands.hybrid_command(aliases=["rm"])
    async def remindme(self, ctx, *text: str):
        try:
            message = ctx.message
            parsed_msg = self.parser.parse(' '.join(text))
            if "all" in parsed_msg:
                await self.get_all_reminders(ctx)
                return
            parsed_time = parsed_msg["remind_time"]
            abs_time = "duration_seconds" not in parsed_time
            now = datetime.now()
            if abs_time:
                today = datetime.combine(datetime.today(),
                                         datetime(hour=12, minute=0, second=0, year=now.year, month=now.month, day=now.day, tzinfo=tz.tzlocal()).time())
                reminder_time = datetime(year=parsed_time.get('year') if parsed_time.get('year') is not None else today.year,
                                         month=parsed_time.get('month') if parsed_time.get(
                                             'month') is not None else today.month,
                                         day=parsed_time.get('day') if parsed_time.get(
                                             'day') is not None else today.day,
                                         hour=parsed_time.get('hour') if parsed_time.get(
                                             'hour') is not None else today.hour,
                                         minute=parsed_time.get('minute') if parsed_time.get(
                                             'minute') is not None else today.minute,
                                         second=parsed_time.get('second') if parsed_time.get(
                                             'second') is not None else today.second,
                                         tzinfo=tz.tzlocal()).timestamp()
            else:
                reminder_time = round(
                    time.time() + float(parsed_time.get("duration_seconds")), 2)
            dt = reminder_time - now.timestamp()
            if dt < 0:
                if dt < 43200:  # less than 12 hrs ago -> remind tomorrow at that time
                    reminder_time += 86400
                else:
                    await ctx.message.reply(
                        "Ich kann dich nicht in der Vergangenheit erinneren"
                    )
                    return

            reason = parsed_msg.get("msg") if parsed_msg.get(
                "msg") is not None else ""

            reminder = Reminder(
                message.id, ctx.channel.id, ctx.author.id, reason, reminder_time
            )
            self.insert_reminder(reminder)
            await message.add_reaction("\N{THUMBS UP SIGN}")
            return
        except Exception as e:
            await ctx.message.reply("Klappt nit lol 🤷")
            logger.error(
                "Remindme Fehler wahrsch falsches Zeitformat?: " + str(e))

    """async def wait_for_reminder(self, reminder: Reminder):
        try:
            if (reminder.time - time.time()) < 0:
                await self.send_reminder(reminder)
            else:
                logger.info("Nächster Reminder geladen: " + str(reminder._id))
                await asyncio.sleep(reminder.time - time.time())
                await self.send_reminder(reminder)
        except Exception as e:
            logger.error(e)"""

    async def check_reminder(self):
        try:
            while True:
                self.cursor.execute(
                    "SELECT * FROM reminders ORDER BY reminder_time ASC LIMIT 1"
                )
                results = self.cursor.fetchall()
                if results:
                    reminder = reminder_from_record(results[0])
                    if (reminder.time - time.time()) < 0:
                        await self.send_reminder(reminder)
                await asyncio.sleep(10)

        except Exception as e:
            logger.error(e)

    async def get_all_reminders(self, ctx):
        try:
            user_id = ctx.author.id
            all_reminders = self.cursor.execute(
                "SELECT * FROM reminders WHERE user_id=? ORDER BY reminder_time ASC",
                (user_id,),
            ).fetchall()
            if not all_reminders:
                await ctx.message.reply(
                    "Du hast keine Reminder, du Megabrain", mention_author=True
                )
            else:
                msg_text = "Ich werde dich demnächst wissen lassen:\n"
                for reminder in all_reminders:
                    remind_dt = datetime.fromtimestamp(reminder[3])
                    remind_date = remind_dt.date().strftime("%d-%b-%Y")
                    remind_time = remind_dt.time().strftime("%H:%M:%S")
                    text = reminder[2]
                    msg_text += "Am **{}** um **{}** werde ich dich wissen lassen, dass:\n**{}**\n\n".format(
                        remind_date, remind_time, text
                    )
                await ctx.message.reply(msg_text, mention_author=True)
        except Exception as e:
            logger.error("Remindme Fehler get_all_reminders(): " + str(e))

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
            logger.error("Remindme Fehler insert_reminder(): " + str(e))

    async def send_reminder(self, reminder: Reminder):
        try:
            if not await self.check_reminder_exists(reminder):
                self.delete_reminder(reminder)
                return
            channel = self.bot.get_channel(reminder.channel_id)
            if reminder.message_id > 0:
                message = await channel.fetch_message(reminder.message_id)
                if reminder.text == "":
                    while True:
                        # satz = json_model.make_short_sentence(140)
                        satz = self.json_model.make_sentence(
                            max_overlap_ratio=0.66,
                        )
                        if satz:
                            reminderText = "Ich werde dich wissen lassen:\n**" + satz + "**"
                            break
                else:
                    if message.author.id == 413068385962819584:
                        reminderText = "**Ali {}**".format(reminder.text)
                    else:
                        reminderText = "Ich werde dich wissen lassen:\n**{}**".format(
                            reminder.text)
            else:
                reminderText = "<@{}>: Ich werde dich wissen lassen:\n**{}**".format(
                    reminder.user_id, reminder.text)
            if (reminder._id != self.global_state.get('reminder_id')):
                self.delete_reminder(reminder)
                self.global_state['reminder_id'] = reminder._id
                logger.info("Auf Reminder geantwortet: " + str(reminder._id))
                await message.reply(reminderText, mention_author=True)
        except Exception as e:
            logger.error(f"Error while sending reminder: {e}")

    async def check_reminder_exists(self, reminder: Reminder):
        try:
            res = self.cursor.execute(
                "SELECT * FROM reminders where id=?", (reminder._id,)
            ).fetchone()
            if not res:
                return False
            if res[6] is not None:
                parent_reminder_record = self.cursor.execute(
                    "SELECT * FROM reminders where id=?", (res[6],)
                ).fetchone()
                if not parent_reminder_record:
                    return False
                try:
                    parent_reminder = reminder_from_record(
                        parent_reminder_record)
                    await self.bot.get_channel(
                        parent_reminder.channel_id
                    ).fetch_message(parent_reminder.message_id)
                    return True
                except:
                    return False
            return True
        except Exception as e:
            logger.error("Remindme Fehler check_reminder_exists(): " + str(e))

    def is_reminder_message(self, message_id, author_id, emoji, user_id):
        try:
            all_reminder_ids = [
                x[0]
                for x in self.cursor.execute(
                    "SELECT message_id FROM reminders"
                ).fetchall()
            ]
            if (
                (message_id not in all_reminder_ids)
                or (str(emoji) != "\N{THUMBS UP SIGN}")
                or (user_id == self.bot.user.id)
                or (user_id == author_id)
            ):
                return False
            return True
        except Exception as e:
            logger.error("Remindme Fehler is_reminder_message(): " + str(e))

    def delete_reminder(self, reminder: Reminder):
        try:
            self.cursor.execute(
                "DELETE FROM reminders WHERE id=?", (reminder._id,))
            self.db.commit()
            logger.info("Reminder gelöscht: " + str(reminder._id))
        except Exception as e:
            logger.error("Remindme Fehler delete_reminder(): " + str(e))


async def setup(bot):
    await bot.add_cog(RemindMe(bot, bot.db, bot.json_model))
