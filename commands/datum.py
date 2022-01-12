import logging
import datetime
import locale
from discord.ext import commands

locale.setlocale(locale.LC_ALL, "de_DE")
logger = logging.getLogger("ZicklaaBot.Datum")


class Datum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def datum(self, ctx):
        try:
            heute = datetime.date.today().strftime("**%d. %B %Y**.")
            tag = datetime.date.today().strftime("**%A**")
            await ctx.reply("Heute ist " + tag + ", der " + heute)
        except Exception as e:
            await ctx.reply("Puh, schwierig")
            logger.error(e)


def setup(bot):
    bot.add_cog(Datum(bot))
