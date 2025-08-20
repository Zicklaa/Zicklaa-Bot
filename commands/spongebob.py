import logging
import discord
from random import choice
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Spongebob")


class Spongebob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def sponge(self, ctx, *text):
        try:
            if not text:
                await ctx.reply(
                    "Bruder gib doch ein Text an was soll das? Verschwendest hier meine CPU Zeit"
                )
            else:
                text = " ".join(text)

                spongified_text = "".join([])
                i = True  # capitalize
                for char in text:
                    if i:
                        spongified_text += char.upper()
                    else:
                        spongified_text += char.lower()
                    if char != " ":
                        i = not i

                embed = discord.Embed(
                    title="", color=16705372, description="**" + spongified_text + "**"
                )
                embed.set_author(
                    name="Spongebob",
                    icon_url="https://cdn.discordapp.com/emojis/658729208515788810.gif",
                )
                embed.set_footer(text="Für " + ctx.author.name)
                await ctx.channel.send(embed=embed)
                await ctx.message.delete()
                logger.info("Spongebob gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.channel.send(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: spongebob()"
            )
            logger.error(f"Request from {ctx.author.name}: {e}")

    @commands.hybrid_command()
    async def randomsponge(self, ctx, *text):
        try:
            if not text:
                await ctx.reply(
                    "Bruder gib doch ein Text an was soll das? Verschwendest hier meine CPU Zeit"
                )
            else:
                text = " ".join(text)

                spongified_text = "".join(
                    choice((str.upper, str.lower))(c) for c in text
                )  # das hier macht random capitalization, sieht schöner aus aber einfach nicht was das Volk will

                embed = discord.Embed(
                    title="", color=16705372, description="**" + spongified_text + "**"
                )
                embed.set_author(
                    name="Spongebob",
                    icon_url="https://cdn.discordapp.com/emojis/658729208515788810.gif",
                )
                embed.add_field(name=spongified_text, value="\u200b")
                embed.set_footer(text="Für " + ctx.author.name)
                await ctx.channel.send(embed=embed)
                await ctx.message.delete()
                logger.info("Spongebob gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.channel.send(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: spongebob()"
            )
            logger.error(f"Request from {ctx.author.name}: {e}")


async def setup(bot):
    await bot.add_cog(Spongebob(bot))
