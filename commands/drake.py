import logging
import os
import random
import discord
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Drake")

dir = "/home/zicklaa/Zicklaa-Bot/static/"


class Drake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drake(self, ctx, *sentences):
        # try:
        if len(sentences) == 2:
            img = Image.open(dir + "drake.jpg")
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            font = ImageFont.truetype(
                dir + "impact.ttf",
                64,
            )
            # draw.text((x, y),"Sample Text",(r,g,b))
            draw.text((900, 300), sentences[0], font=font, fill="#000")
            draw.text((900, 900), sentences[1], font=font, fill="#000")
            img.save(dir + "drake-out.jpg")
            await ctx.channel.send(file=discord.File(dir + "drake-out.jpg"))
            await ctx.message.delete()
            logger.info("Drake gepostet für: " + ctx.author.name)

        else:
            await ctx.reply("Bidde gib 2 Optionen")
            logger.info("Drake ERROR für: " + ctx.author.name)

        """except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Drake ERROR von {ctx.author.name}: {e}")"""


def setup(bot):
    bot.add_cog(Drake(bot))
