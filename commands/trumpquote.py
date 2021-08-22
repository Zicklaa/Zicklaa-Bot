import logging
import discord
from discord.ext import commands
import requests

logger = logging.getLogger("ZicklaaBot.TrumpQuote")


class TrumpQuote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Vermutlich machts Sinn Error handling zu machen wenn nix von der Api zurückkommt aber bin ich zu faul für
    async def get_random_quote(self):
        api_response = requests.get(
            'https://api.tronalddump.io/random/quote').json()
        return api_response['value']

    async def build_embedd(ctx, quote):
        embed = discord.Embed(title="", color=16705372, description=quote)
        embed.set_footer(text='- Donald Trump')
        embed.set_thumbnail(
            url="https://img.welt.de/img/politik/ausland/mobile232680235/9402500987-ci102l-w1024/Donald-Trump.jpg")
        return embed

    @commands.command()
    async def trump(self, ctx, *text):
        try:
            message = await self.get_random_quote()
            embed = await self.build_embedd(message)
            await ctx.reply(embed=embed)
            logger.info("Trumpquote gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Kurwa iwas kaputt")
            logger.error(f"Trumpquote from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(TrumpQuote(bot))
