import logging
import os, random
import discord

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Choose")

dir = "/home/pi/Zicklaa-Bot/LustigeBildchen/"

class LustigeBildchen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ltb(self, ctx):
        try:
            ltb = random.choice(os.listdir(dir))
            await ctx.channel.send(file=discord.File(dir + ltb))
            await ctx.message.delete()
            logger.info("Lustiges Bildchen gepostet für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Lustiges Bilchen ERROR von {ctx.author.name}: {e}")
        pass


def setup(bot):
    bot.add_cog(LustigeBildchen(bot))
