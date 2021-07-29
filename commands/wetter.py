import logging
import urllib.request

import discord
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Wetter")


class Wetter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wetter(self, ctx, location: str):
        try:
            '''url = 'https://wttr.in/{}'.format(place) + "?n&T&2&lang=de"
            res = requests.get(url)
            await message.channel.send(
                "```" + res.text.replace("Folgen Sie https://twitter.com/igor_chubin für wttr.in Updates", "") + "```")'''
            url_png = 'https://de.wttr.in/{}'.format(location) + "_m" + ".png"
            urllib.request.urlretrieve(url_png,
                                       "wetter.png")

            await ctx.channel.send(file=discord.File(r'wetter.png'))
            logger.info('Wetter gepostet für ' + ctx.author.name + ': ' + location)
        except:
            await ctx.channel.send(
                'Wetter schmetter, sag ich schon immer.')
            logger.error('ERROR: Wetter für ' + ctx.author.name)


def setup(bot):
    bot.add_cog(Wetter(bot))
