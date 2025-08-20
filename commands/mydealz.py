import logging
import os
import requests

from discord.ext import commands
from bs4 import BeautifulSoup

logger = logging.getLogger("ZicklaaBot.MyDealz")
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61"
}


class MyDealz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def mdc(self, ctx):
        try:
            response = requests.get("https://www.mydealz.de/deals", headers=header)
            soup = BeautifulSoup(response.content, "html.parser")
            hot3 = ""
            for link in soup.findAll(
                "a", {"class": "cept-tt thread-link linkPlain thread-title--list"}
            )[:3]:
                hot3 = hot3 + link["href"] + "\n"
            await ctx.reply(hot3)
            logger.info("MyDealz für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Puh, schwierig")
            logger.error(f"Request from {ctx.author.name}. MyDealz.")

    @commands.hybrid_command()
    async def mdd(self, ctx):
        try:
            response = requests.get("https://www.mydealz.de", headers=header)
            soup = BeautifulSoup(response.content, "html.parser")
            hot3 = ""
            for link in soup.findAll(
                "a", {"class": "cept-tt thread-link linkPlain thread-title--list"}
            )[:3]:
                hot3 = hot3 + link["href"] + "\n"
            await ctx.reply(hot3)
            logger.info("MyDealz für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Puh, schwierig")
            logger.error(f"Request from {ctx.author.name}. MyDealz.")


async def setup(bot):
    await bot.add_cog(MyDealz(bot))
