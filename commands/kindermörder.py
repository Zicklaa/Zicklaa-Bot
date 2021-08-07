import logging
import discord
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Kindermörder")


class Kindermörder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kindermörder(self, ctx):
        try:
            file = discord.File("raul.gif")
            await ctx.channel.send(file=file, content="RAUL CRUISEHAUSEN KINDERMÖRDER")
            await ctx.message.delete()
            logger.info("Kindermörder gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.reply(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: kindermörder()"
            )
            logger.error(f"Kindermörder from {ctx.author.name}: {e}")

    @commands.command()
    async def kühlschrank(self, ctx):
        try:
            file = discord.File("raul2.gif")
            await ctx.channel.send(file=file)
            await ctx.message.delete()
            logger.info("Kindermörder gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.reply(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: kindermörder()"
            )
            logger.error(f"Kindermörder from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Kindermörder(bot))
