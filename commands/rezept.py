import logging
import random

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Rezept")


class Rezept(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def rezept(self, ctx):
        try:
            rezepte_channel = await self.bot.fetch_channel(860154286141997056)
            rezepte_pins = await rezepte_channel.pins()
            rezept = random.choice(rezepte_pins)
            message_link = "https://discord.com/channels/{}/{}/{}".format(
                rezept.guild.id, rezept.channel.id, rezept.id
            )
            await ctx.reply(message_link)
            pass
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(e)
        pass


async def setup(bot):
    await bot.add_cog(Rezept(bot))
