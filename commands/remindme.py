import asyncio
import logging
import time
from datetime import datetime

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.RemindMe")


class RemindMe(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.cursor = db.cursor()

    @commands.command()
    async def remindme(self, ctx, method: str, *text: str):
        message = ctx.message
        unit_to_second = {"s": 1, "m": 60, "h": 60 * 60, "d": 60 * 60 * 24, "w": 60 * 60 * 24 * 7,
                          "mon": 60 * 60 * 24 * 7 * 30}
        if method == 'all':
            await self.get_all_reminders(ctx)
            return
        elif method.isdigit():
            digits = method
            unit = text[0]
            reason = " ".join(text[1:])
        else:
            unit = method[-1]
            digits = method[:-1]
            reason = " ".join(text)

        reminder_time = round(time.time() + (float(int(digits) * int(unit_to_second[unit]))), 2)
        sql = "INSERT INTO reminders (user_id, reminder_text, reminder_time, channel, message_id) VALUES (?, ?, ?, ?, ?)"
        val = (ctx.author.id, reason, reminder_time, ctx.channel.id, ctx.message.id)
        self.cursor.execute(sql, val)
        self.db.commit()
        self.cursor.execute("SELECT id FROM reminders WHERE reminder_time=?", (reminder_time,))
        id = self.cursor.fetchall()[0][0]
        logger.info('Neuer Reminder in die DB gepusht: ' + str(id))
        channel = ctx.channel.id
        await message.add_reaction('\N{THUMBS UP SIGN}')
        logger.info('reminder(): Thumbs Up auf Nachricht reagiert')
        await self.wait_for_reminder(ctx.author.id, reason, reminder_time, message, channel, id)

    async def wait_for_reminder(self, user_id, reminder_text, reminder_time1, message, channel, id):
        try:
            if (reminder_time1 - time.time()) < 0:
                try:
                    await message.reply(
                        "Ich werde dich wissen lassen:\n**{}**".format(reminder_text), mention_author=True)
                    logger.info('Auf Reminder geantortet: ' + str(id))
                except:
                    await channel.send(
                        "<@{}>: Ich werde dich wissen lassen:\n**{}**".format(user_id, reminder_text))
                    logger.info('Auf Reminder geantortet: ' + str(id))
                self.cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
                self.db.commit()
                logger.info('Reminder gelöscht: ' + str(id))
            else:
                logger.info('Nächster Reminder geladen: ' + str(id))
                await asyncio.sleep(reminder_time1 - time.time())
                try:
                    await message.reply(
                        "Ich werde dich wissen lassen:\n**{}**".format(reminder_text), mention_author=True)
                    logger.info('Auf Reminder geantortet: ' + str(id))
                except:
                    await channel.send(
                        "<@{}>: Ich werde dich wissen lassen:\n**{}**".format(user_id, reminder_text))
                    logger.info('Auf Reminder geantortet: ' + str(id))
                self.cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
                self.db.commit()
                logger.info('Reminder gelöscht: ' + str(id))
        except:
            await message.channel.send(
                'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wait_for_reminder()')
            logger.error('wait_for_reminder()')

    async def get_reminder_startup(self):
        try:
            self.cursor.execute("SELECT * FROM reminders ORDER BY reminder_time ASC LIMIT 1")
            result = self.cursor.fetchall()
            if result:
                id = result[0][0]
                user_id = result[0][1]
                reminder_text = result[0][2]
                reminder_time1 = result[0][3]
                channel_id = result[0][4]
                channel = self.bot.get_channel(channel_id)
                try:
                    message = await channel.fetch_message(id=result[0][5])
                except:
                    logger.info('Nächster Reminder geladen')
                    await asyncio.sleep(reminder_time1 - time.time())
                    await channel.send(
                        "<@{}>: Ich werde dich wissen lassen:\n**{}**".format(user_id, reminder_text))
                    self.cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
                    self.db.commit()
                    logger.info('Reminder gelöscht')
                    await self.get_reminder_startup()
                await self.wait_for_reminder_startup(id, reminder_text, reminder_time1, channel_id, message)
        except:
            await message.channel.send(
                'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: get_reminder_startup()')
            logger.error('get_reminder_startup()')

    async def wait_for_reminder_startup(self, id, reminder_text, reminder_time1, channel_id, message):
        try:
            channel = self.bot.get_channel(channel_id)
            if (reminder_time1 - time.time()) < 0:
                await message.reply(
                    "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
                logger.info('Auf Reminder geantortet: ' + str(id))
                self.cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
                self.db.commit()
                logger.info('Reminder gelöscht: ' + str(id))
            else:
                logger.info('Nächster Reminder geladen: ' + str(id))
                await asyncio.sleep(reminder_time1 - time.time())
                await message.reply(
                    "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
                logger.info('Auf Reminder geantortet: ' + str(id))
                self.cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
                self.db.commit()
                logger.info('Reminder gelöscht: ' + str(id))
            await self.get_reminder_startup()
        except:
            await channel.send(
                'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wait_for_reminder_startup()')
            logger.error('wait_for_reminder_startup() von ' + message.author.name)
    
    async def get_all_reminders(self,ctx):
        user_id = ctx.author.id
        all_reminders = self.cursor.execute("SELECT * FROM reminders WHERE user_id=? ORDER BY reminder_time ASC",(user_id,)).fetchall()
        if not all_reminders:
            await ctx.message.reply("Du hast keine Reminder, du Megabrain",mention_author=True)
        else:
            msg_text = "Ich werde dich demnächst wissen lassen:\n".format(user_id)
            for reminder in all_reminders:
                remind_dt = datetime.fromtimestamp(reminder[3])
                remind_date = remind_dt.date().strftime("%d-%b-%Y")
                remind_time = remind_dt.time().strftime("%H:%M:%S")
                text = reminder[2]
                msg_text += "Am **{}** um **{}** werde ich dich wissen lassen, dass:\n**{}**\n\n".format(remind_date,remind_time,text)
            await ctx.message.reply(msg_text,mention_author=True)

def setup(bot):
    bot.add_cog(RemindMe(bot, bot.db))
