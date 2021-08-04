import logging
import os, random
import discord
from discord import message
import markovify
import re

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Hivemind")

with open('hivemind.txt','r',encoding='utf-8') as f:
    text = f.read()
text_model = markovify.NewlineText(text, state_size=3)
text_model = text_model.compile()
print("compiled")

class Hivemind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hivemind(self, ctx):
        try:
            while True:
                satz = text_model.make_short_sentence(140)
                if satz:
                    await ctx.reply(satz)
                    break

            logger.info("Hivemind für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")

    '''@commands.command()
    async def scrap(self, ctx):
        try:
            print("scrapping")
            messages = await ctx.channel.history(limit=5000).flatten()
            f = open("hivemind.txt", "a")
            for message in messages:
                f.write(message.content + "\n")
            f.close()
            print("done")
            #logger.info("Hivemind Scrap für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            # logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")'''


def setup(bot):
    bot.add_cog(Hivemind(bot))
