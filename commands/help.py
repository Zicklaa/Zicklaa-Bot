import discord
import logging
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.BenWach")

class Help(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Help', description='Hier wird Ihnen geholfen!', color=0x00ff00)
        embed.add_field(name='+help', value="Öffnet das Hilfefenster", inline=False)
        embed.add_field(name='+lyrics', value="Format: +lyrics (full/link) [USERNAME]",
                        inline=False)
        embed.add_field(name='+wetter', value="Format: +wetter [ORTNAME]", inline=False)
        embed.add_field(name='+asciiwetter', value="Format: +asciiwetter [ORTNAME]", inline=False)
        embed.add_field(name='+wiki', value="Format: +wiki [SUCHBEGRIFF]", inline=False)
        embed.add_field(name='+wishlist', value="Format: +wishlist [WUNSCH]", inline=False)
        embed.add_field(name='+showlist', value="Zeigt die Wunschliste an", inline=False)
        embed.add_field(name='+delwish', value="+delwish [ID] (nur für coole Menschen tho)", inline=False)
        embed.add_field(name='+remindme',
                        value="Format: +remindme <all | [ZAHL][s/m/h/d/mon]> [TEXT]",
                        inline=False)
        embed.add_field(name='+spongebob', value="+spongebob [TEXT]", inline=False)
        embed.add_field(name='+randomsponge', value="+randomsponge [TEXT]", inline=False)
        embed.add_field(name='+git', value="Poschded den link zum Github Repository", inline=False)
        embed.add_field(name='+benwach', value="Ben wach?", inline=False)
        embed.add_field(name='+magic8', value="+magic8 [FRAGE]", inline=False)
        embed.add_field(name='+choose',
                        value='+choose [Option 1] [Option 2] [...]\nBei mehreren Wörtern pro Option bitte jede Option in " " setzen.',
                        inline=False)
        embed.set_author(name='Gott', icon_url='https://cdn.psychologytoday.com/sites'
                                               '/default/files/field_blog_entry_images/God_the_Father.jpg')
        await self.get_destination().send(embed=embed)
