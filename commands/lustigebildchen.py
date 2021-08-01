import logging
import os, random
import discord

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Choose")


class LustigeBildchen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ltb(self, ctx):
        try:
            ltb = random.choice(os.listdir("/home/pi/Zicklaa-Bot/LustigeBildchen/"))
            await ctx.channel.send(file=discord.File("/home/pi/Zicklaa-Bot/LustigeBildchen/" + ltb))
            await ctx.message.delete()
            logger.info("Lustiges Bildchen gepostet für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(e)
        pass


def setup(bot):
    bot.add_cog(LustigeBildchen(bot))
