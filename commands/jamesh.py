import asyncio
import logging

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.JamesH")


class JamesH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jamesh(self, ctx):
        try:
            await ctx.message.delete()
            await ctx.send("Da gibt es ein James Hoffmann Video dazu.")
        except Exception as e:
            await ctx.reply(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: JamesH()"
            )
            logger.error(f"JamesH from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(JamesH(bot))
