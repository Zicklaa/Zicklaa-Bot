import logging
import random

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Choose")


class Choose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *options):
        try:

            if len(options) < 1:
                await ctx.channel.send("Gib Optionen, Moruk")
            else:
                cleared_list = []
                for item in options:
                    if item == " " or item == "":
                        pass
                    else:
                        cleared_list.append(item)
                if len(cleared_list) < 2:
                    await ctx.channel.send("Gib mehr als 1 Optionen, Moruk")
                    logger.error("choose(): Zu wenig Optionen gegeben")
                else:
                    choice = random.choice(cleared_list)
                    await ctx.channel.send(
                        "Oh magische Miesmuschel! Wie lautet deine Antwort? \n" + "**" + choice + "**")
                    logger.info("choose(): Antwort gepostet für: " + ctx.author.name)

        except:
            await ctx.channel.send("Klappt nit lol 🤷")
            logger.error('choose()')
        pass


def setup(bot):
    bot.add_cog(Choose(bot))