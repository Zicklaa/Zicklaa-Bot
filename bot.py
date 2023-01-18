import discord
import config
import discord
from discord.ext import commands
import sqlite3
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import traceback
import sys
import random
import json
import markovify
import re


def create_log_file(path):
    logger = logging.getLogger("ZicklaaBot")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        path, when="midnight", interval=1, backupCount=5)
    formatter = logging.Formatter(
        "%(asctime)s::%(name)s::%(funcName)s::%(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = create_log_file("ZicklaaBotLog.log")

user_last_command = {}

initial_extensions = [
    "commands.admin",
    "commands.chefkoch",
    "commands.choose",
    "commands.datum",
    "commands.discordle",
    "commands.fav",
    "commands.git",
    "commands.girlboss",
    "commands.help",
    "commands.hivemind",
    "commands.kindermörder",
    "commands.lyrics",
    "commands.magic8",
    "commands.mydealz",
    "commands.obm",
    "commands.ofen",
    "commands.poll",
    "commands.quote",
    "commands.remindme",
    "commands.rezept",
    "commands.roll",
    "commands.star",
    "commands.spongebob",
    "commands.translate",
    "commands.trumpquote",
    "commands.wetter",
    "commands.wishlist",
    "commands.wiki",
    # "commands.voice",
    # "commands.urban",
    # "commands.urbancog",
]


class ZicklaaBot(discord.ext.commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents, command_prefix=config.PREFIX, help_command=None)
        self.db = sqlite3.connect(
            "/home/zicklaa/Zicklaa-Bot/reminder-wishlist.db")
        self.LASTFM_API_KEY = config.API_KEY
        self.LASTFM_API_SECRET = config.API_SECRET
        self.LYRICS_KEY = config.LYRICS_KEY
        self.CLIENT_ID = config.CLIENT_ID
        self.CLIENT_SECRET = config.CLIENT_SECRET
        self.RAPID_HOST = config.RAPID_HOST
        self.RAPID_KEY = config.RAPID_KEY
        self.create_tables()
        self.json_model = json_model()

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}: {e}")

    async def on_ready(self):
        print("Hallo I bim omnline :^)")
        logger.info(
            "=======================Startup=========================")
        remindme = self.get_cog("RemindMe")
        await remindme.check_reminder()

    def create_tables(self):
        try:
            cursor = self.db.cursor()
            creation1 = """CREATE TABLE IF NOT EXISTS
            reminders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, reminder_text TEXT, reminder_time INTEGER, channel INTEGER, message_id INTEGER)"""
            cursor.execute(creation1)
            reminder_columns = [
                x[1] for x in cursor.execute("PRAGMA table_info(reminders)").fetchall()
            ]
            if not "parent_id" in reminder_columns:
                alter1 = """ALTER TABLE reminders ADD COLUMN parent_id INTEGER"""
                cursor.execute(alter1)
            creation2 = """CREATE TABLE IF NOT EXISTS wishlist(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, wishtext TEXT, ts TEXT)"""
            cursor.execute(creation2)
            creation3 = """CREATE TABLE IF NOT EXISTS favs(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, message_id INTEGER, name TEXT, channel_id INTEGER)"""
            cursor.execute(creation3)
            creation4 = """CREATE TABLE IF NOT EXISTS stars(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER)"""
            cursor.execute(creation4)
        except:
            pass


def json_model():
    with open('/home/zicklaa/Zicklaa-Bot/static/hivemind.json', encoding="utf-8") as json_file:
        hivemind_json = json.load(json_file)
    json_model = markovify.Text.from_json(hivemind_json)
    print("hivemind.json loaded")
    return json_model


bot = ZicklaaBot()


# Cooldown check
@bot.check
async def is_on_cooldown(ctx):
    global user_last_command
    if str(ctx.author) not in user_last_command:
        user_last_command[str(ctx.author)] = 10
    elapsed = time.time() - user_last_command[str(ctx.author)]
    if elapsed > 2:
        user_last_command[str(ctx.author)] = time.time()
        return True
    return False


@bot.event
async def on_message(message):
    if not message.author.id == 571051961256902671:
        if random.random() < config.SECRET_PROBABILITY:
            if "crazy" in message.content.lower():
                await message.reply(message.content.lower().replace("crazy", "***normal***"))
            elif "kult" in message.content.lower():
                await message.reply("***KEIN KULT***")
            elif message.content.lower() == "hi":
                await message.reply("Hallo!")
            elif message.content.lower() == "lol":
                await message.reply("xD")
            elif message.content.lower() == "xd":
                await message.reply("lol")
            elif message.content.lower() == "uff":
                await message.reply("uff")
            elif message.content.lower() == "gumo":
                await message.reply("GuMo")
            elif re.search(r'\bdanke\b', message.content.lower()) is not None:
                await message.reply("Bitte!")
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, "on_error"):
        return
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    ignored = (commands.CommandNotFound,)
    error = getattr(error, "original", error)

    if isinstance(error, ignored):
        return

    if isinstance(error, commands.errors.CheckFailure):
        logger.error(f"User {str(ctx.author)} triggered: {error}")
        return
    else:
        print("Ignoring exception in command {}:".format(
            ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )


bot.run(config.CLIENT_RUN)
