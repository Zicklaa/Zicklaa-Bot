from discord.ext import commands
import logging
from datetime import datetime

logger = logging.getLogger("ZicklaaBot.BenWach")

class BenWach(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def benwach(self,ctx):
        try:
            current_hour = datetime.now().hour
            if 0 <= current_hour < 6:
                await ctx.message.reply("Ben ist wahrscheinlich grad wach :))")
            elif 6 <= current_hour < 14:
                await ctx.message.reply("Spinnst du? Hast du mal auf die Uhr gekuckt?")
            elif 14 <= current_hour < 24:
                await ctx.message.reply("Ben ist wahrscheinlich grad wach :))")
        except:
            await ctx.channel.send('Irgendwas stimmt nicht, Mois')
            logger.error('benwach: Fehler')


def setup(bot):
    bot.add_cog(BenWach(bot))