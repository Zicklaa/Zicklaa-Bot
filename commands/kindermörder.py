import logging
import discord
from discord.ext import commands
from config import globalPfad

logger = logging.getLogger("ZicklaaBot.Kindermörder")


class Kindermörder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def kindermörder(self, ctx):
        try:
            file = discord.File(globalPfad + "static/raul.gif")
            await ctx.channel.send(file=file, content="RAUL CRUISEHAUSEN KINDERMÖRDER")
            await ctx.message.delete()
            logger.info("Kindermörder gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.reply(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: kindermörder()"
            )
            logger.error(f"Kindermörder from {ctx.author.name}: {e}")

    @commands.hybrid_command()
    async def raul(self, ctx):
        try:
            await ctx.channel.send(
                "https://cdn.discordapp.com/attachments/122739462210846721/873703041889607720/raul2.gif"
            )
            await ctx.message.delete()
            logger.info("Kindermörder gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.reply(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: kindermörder()"
            )
            logger.error(f"Kindermörder from {ctx.author.name}: {e}")


async def setup(bot):
    await bot.add_cog(Kindermörder(bot))
