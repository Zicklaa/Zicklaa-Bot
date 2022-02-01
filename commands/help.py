import discord
import logging
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Help")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help", description="Hier wird Ihnen geholfen!", color=0x00FF00
        )
        # embed.add_field(name="+benwach", value="Ben wach?", inline=False)
        embed.add_field(
            name="+choose", value='+choose [Option 1] [Option 2] [...]\nBei mehreren Wörtern pro Option bitte jede Option in " " setzen.', inline=False)
        embed.add_field(
            name="+ck", value='+ck [Zutat] ODER +ck [rotd] für das Rezept des Tages!', inline=False)
        embed.add_field(
            name="+datum", value='Welchen Tag haben wir heute?', inline=False)
        embed.add_field(
            name="+fav", value="Faven mit 🦶, Löschen mit 🗑️\nFormat: +fav [FAV NAME] | +allfavs", inline=False)
        embed.add_field(
            name="+git", value="Poschded den link zum Github Repository", inline=False)
        embed.add_field(
            name="+help", value="Öffnet das Hilfefenster", inline=False)
        embed.add_field(
            name="+hm", value="Was würde der Benserver dazu sagen?", inline=False)
        embed.add_field(name="+kindermörder | +raul",
                        value="RAUL CRUISEHAUSEN KINDERMÖRDER", inline=False)
        embed.add_field(
            name="+ltb", value="Postet (L)us(T)ige (B)ildchen", inline=False)
        embed.add_field(
            name="+lyrics", value="Format: +lyrics (full/link) [USERNAME]", inline=False)
        embed.add_field(name="+magic8", value="+magic8 [FRAGE]", inline=False)
        embed.add_field(
            name="+mdc/mdd", value="+mdc für die aktuell heißesten Dealz und +mdd für 3 heißesten ~~Singles~~ Dealz des Tages.", inline=False)
        embed.add_field(
            name="+ofen", value="Mariam only >:(", inline=False)
        embed.add_field(name="+obm | +oow | +obr | +ali" ,
                        value="Postet ein  Random Meme aus hot von r/OkBrudiMongo oder dem Ösi/US Pendant", inline=False)
        embed.add_field(
            name="+remindme / +rm", value="Format: +remindme/rm <all | [ZAHL][s/m/h/d/mon]> [TEXT]", inline=False)
        embed.add_field(
            name="+rezept", value="Random Rezept aus #durst-auf-wurst", inline=False)
        embed.add_field(name="+sponge",
                        value="+sponge/randomsponge [TEXT]", inline=False)
        embed.add_field(
            name="+wetter", value="Format: +wetter/asciiwetter [ORTNAME]", inline=False)
        embed.add_field(
            name="+wiki", value="Format: +wiki [SUCHBEGRIFF]", inline=False)
        embed.add_field(
            name="+wishlist", value="Format: +wishlist [WUNSCH] | +showlist", inline=False)

        embed.set_author(
            name="Gott",
            icon_url="https://cdn.psychologytoday.com/sites"
            "/default/files/field_blog_entry_images/God_the_Father.jpg",
        )
        dm_channel = await ctx.author.create_dm()
        await ctx.message.delete()
        await dm_channel.send(embed=embed)
        # await self.get_destination().send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
