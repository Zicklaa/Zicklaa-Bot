import logging
import random
import discord
import datetime
from dateutil import tz
import pytz

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Quote")


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx, link):
        try:
            if link:
                try:
                    link = link.split("/")
                    server_id = int(link[4])
                    channel_id = int(link[5])
                    msg_id = int(link[6])
                    server = self.bot.get_guild(server_id)
                    channel = self.bot.get_channel(channel_id)
                    message = await channel.fetch_message(msg_id)
                    embed = discord.Embed(
                        title="", description=message.content, color=0x00ff00)
                    current_time = (pytz.utc.localize(message.created_at).astimezone(tz.tzlocal())
                                    ).strftime("%d.%m.%Y, %H:%M:%S")
                    if message.attachments:
                        embed.set_image(
                            url=str(message.attachments[0].url))
                    embed.set_author(
                        name=message.author.name, icon_url=message.author.avatar_url, url=message.jump_url)
                    embed.set_footer(
                        text=current_time + ' | #' + message.channel.name + " | Quoted by: " + ctx.author.name)
                    await ctx.channel.send(embed=embed)
                    await ctx.message.delete()

                    logger.info("quote(): Quote gepostet für: " +
                                ctx.author.name)
                except Exception as e:
                    await ctx.reply("Link br0ke 🤷")
                    logger.error(f"Quote from {ctx.author.name}: {e}")
            else:
                await ctx.reply(
                    "Wie soll ich das quoten wenn du nichtmal ne Link gibst, du Monger?"
                )
                logger.info(
                    "Quote(): Kein Link gegeben von: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Quote from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Quote(bot))
