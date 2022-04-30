import logging
from deep_translator import GoogleTranslator

import discord
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Translate")


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, *text):
        async with ctx.channel.typing():
            try:
                text = " ".join(text)
                if len(text) > 950:
                    await ctx.reply("Text zu lang lol")
                    logger.info("Translate zu lang für " +
                                ctx.author.name)
                else:
                    translated = GoogleTranslator(source='auto', target='de').translate(text)

                    await ctx.reply("**Original: **" + text + "\n" + "\n" + "**Übersetzt: **" + translated)
                    logger.info("Translate gepostet für " +
                                ctx.author.name)
            except Exception as e:
                await ctx.reply("Kann kein Italienisch :/")
                logger.error(f"Translate Error from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Translate(bot))
