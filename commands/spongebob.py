import logging
import discord
from random import choice
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Git")


class Spongebob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spongebob(self, ctx, *text):
        try:
            if not text:
                await ctx.reply(
                'Bruder gib doch ein Text an was soll das? Verschwendest hier meine CPU Zeit')
            else:
                text = " ".join(text)
                # spongified_text = ''.join(choice((str.upper, str.lower))(c) for c in text)  # dashier macht random capitalization, sieht schöner aus aber einfach nicht was das volk will
            
                spongified_text = ""
                i = True  # capitalize
                for char in text:
                    if i:
                        spongified_text += char.upper()
                    else:
                        spongified_text += char.lower()
                    if char != ' ':
                        i = not i

                embed = discord.Embed(title='', color=16705372)
                embed.set_author(name="Spongebob", icon_url="https://cdn.discordapp.com/emojis/658729208515788810.gif")
                embed.add_field(name=spongified_text, value="\u200b")
                embed.set_footer(text="Für " + ctx.author.name)
                await ctx.reply(embed=embed)
                logger.info('Spongebob gepostet für ' + ctx.author.name)
        except:
            await ctx.channel.send(
                'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: spongebob()')
            logger.error('Spongebob von ' + ctx.author.name)


def setup(bot):
    bot.add_cog(Spongebob(bot))