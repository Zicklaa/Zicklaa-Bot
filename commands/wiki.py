import logging
import urllib.request

import discord
from bs4 import BeautifulSoup
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Wiki")


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wiki(self, ctx, *search_term):
        async with ctx.channel.typing():
            try:
                if search_term[0] == 'feet':
                    await self.wikifeet(ctx)
                    pass
                wiki1 = " ".join(search_term)
                wiki2 = "_".join(search_term)
                url = 'https://de.wikipedia.org/wiki/' + wiki2.title()
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, "html.parser")
                embed = discord.Embed(title=wiki1.title(), url=url, color=0x00ff00)
                start = soup('p')
                x = 0
                text2 = ""
                for i in start:
                    t = str(i.getText())
                    if len(t) > 200:
                        text = str(i.getText())
                        text2 = text2 + text
                        x = x + 1
                    if x == 2:
                        break
                text2 = (text2[:1020] + '...') if len(text2) > 1024 else text2
                text2 = text2.replace('[1]', '').replace('[2]', '').replace('[3]', '').replace('[4]', '') \
                    .replace('[5]', '').replace('[6]', '').replace('[7]', '') \
                    .replace('[8]', '').replace('[9]', '').replace('[10]', '')
                embed.add_field(name="Beschreibung", value=text2, inline=False)

                image_tag = soup.findAll('img')
                for bild in image_tag:
                    bild_url = 'https:' + bild.get('src')
                    if bild_url == 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Disambig-dark.svg/25px' \
                                '-Disambig-dark.svg.png' or bild_url == 'https://upload.wikimedia.org/wikipedia/c' \
                                                                        'ommons/thumb/f/f3/Photo-request.svg/40px-P' \
                                                                        'hoto-request.svg.png' or \
                            bild_url == 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Qsicon_lesenswert.' \
                                        'svg/15px-Qsicon_lesenswert.svg.png' or bild_url == 'https://upload.wikimedia.' \
                                                                                            'org/wikipedia/commons/thumb' \
                                                                                            '/a/a1/Qsicon_gesprochen.svg/' \
                                                                                            '15px-Qsicon_gesprochen.' \
                                                                                            'svg.png' or bild_url == \
                            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/' \
                            'Wiktfavicon_en.svg/16px-Wiktfavicon_en.svg.png':
                        pass
                    else:
                        bild_url = 'https:' + bild.get('src')
                        embed.set_thumbnail(url=bild_url)
                        break
                await ctx.reply(embed=embed)
                logger.info('Wikiartikel gepostet für ' + ctx.author.name + ': ' + wiki1)
            except Exception as e:
                if search_term[0] != "feet":
                    wiki1 = " ".join(search_term)
                    wiki2 = "_".join(search_term)
                    wiki22 = wiki2.title()
                    url = 'https://de.wikipedia.org/wiki/' + wiki22
                    await ctx.reply('Jibtet nit. Probier doch mal selber: ' + url)
                    logger.error(f'Request from {ctx.author.name}: {e}')

    @commands.command()
    async def wikifeet(self, ctx, *args):
        await ctx.reply(
            'https://images.squarespace-cdn.com/content/v1/51323aa1e4b0b73e528cb71c/1567786369681-938Z512OX2Z03BDUGU62/Monty-Python-foot-1024x803.jpg')
        logger.info('Wikifeet gepostet für ' + ctx.author.name)


def setup(bot):
    bot.add_cog(Wiki(bot))
