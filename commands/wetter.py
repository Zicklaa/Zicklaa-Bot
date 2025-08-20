import logging
import urllib.request
import requests
from config import globalPfad
import discord
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Wetter")


class Wetter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def wetter(self, ctx, location: str):
        async with ctx.channel.typing():
            try:
                """url = 'https://wttr.in/{}'.format(place) + "?n&T&2&lang=de"
                res = requests.get(url)
                await message.channel.send(
                    "```" + res.text.replace("Folgen Sie https://twitter.com/igor_chubin für wttr.in Updates", "") + "```")
                """
                url_png = "https://de.wttr.in/{}".format(
                    location) + "_m" + ".png"
                urllib.request.urlretrieve(
                    url_png, globalPfad + "static/wetter.png"
                )
                await ctx.reply(
                    file=discord.File(globalPfad + "static/wetter.png")
                )
                logger.info("Wetter gepostet für " +
                            ctx.author.name + ": " + location)
            except Exception as e:
                await ctx.reply("Wetter schmetter, sag ich schon immer.")
                logger.error(f"Request from {ctx.author.name}: {e}")

    @commands.hybrid_command()
    async def asciiwetter(self, ctx, location: str):
        async with ctx.channel.typing():
            try:
                url = "https://wttr.in/{}".format(location) + "?n&T&2&lang=de"
                res = requests.get(url)
                await ctx.reply(
                    "```"
                    + res.text.replace(
                        "Folgen Sie https://twitter.com/igor_chubin für wttr.in Updates",
                        "",
                    )
                    + "```"
                )
                logger.info(
                    "Ascii Wetter gepostet für " + ctx.author.name + ": " + location
                )
            except Exception as e:
                await ctx.reply("Wetter schmetter, sag ich schon immer.")
                logger.error(f"Request from {ctx.author.name}: {e}")


async def setup(bot):
    await bot.add_cog(Wetter(bot))
