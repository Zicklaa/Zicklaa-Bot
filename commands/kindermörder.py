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
            await ctx.reply(file=file, content="RAUL CRUISEHAUSEN KINDERMÖRDER")
            '''await ctx.reply("RAUL CRUISEHAUSEN KINDERMÖRDER")
            await ctx.channel.send("https://media.discordapp.net/attachments/122739462210846721/809326868989870110/ezgif-2-25ca1215409f.gif")'''
            logger.info("Kindermörder gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.reply(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: kindermörder()"
            )
            logger.error(f"Kindermörder from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Kindermörder(bot))
