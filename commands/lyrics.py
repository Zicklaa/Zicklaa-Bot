import logging

import discord
import lyricsgenius
import pylast
from discord.ext import commands
from lyricsgenius import Genius

logger = logging.getLogger("ZicklaaBot.Lyrics")


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_f2_in_concert(ctx):
        return ctx.channel.id == 608746970340786282

    @commands.command()
    #@commands.check(is_f2_in_concert)
    async def lyrics(self, ctx, method: str, username: str):
        async with ctx.channel.typing():
            try:
                network = pylast.LastFMNetwork(api_key=self.bot.LASTFM_API_KEY, api_secret=self.bot.LASTFM_API_SECRET)
                user = network.get_user(username)
            except Exception as e:
                await ctx.channel.send('User nit gefunden.')
                logger.error(f'Request from {ctx.author.name}: {e}')
                return
            if method == 'full':
                try:
                    lied = user.get_now_playing()
                    seconds = (lied.get_duration() / 1000) % 60
                    seconds = int(seconds)
                    minutes = (lied.get_duration() / (1000 * 60)) % 60
                    minutes = int(minutes)
                    if seconds < 10:
                        seconds = "0" + str(seconds)

                    artisturl = 'https://www.last.fm/de/music/' + str(lied.get_artist()).replace(' ', '+')
                    songurl = artisturl + '/_/' + str(lied.get_name()).replace(' ', '+').replace('/', '%2F')
                    name = str('[' + str(lied.get_name()) + '](' + str(songurl) + ')')
                    artist = str('[' + str(lied.get_artist()) + '](' + str(artisturl) + ')')

                    embed = discord.Embed(title='', color=1917791)

                    if user.get_image() is not None:
                        embed.set_author(name=username, icon_url=user.get_image(),
                                        url='https://www.last.fm/user/' + username)
                    else:
                        embed.set_author(name=username, url='https://www.last.fm/user/' + username)

                    embed.set_thumbnail(url=str(lied.get_cover_image()))
                    embed.add_field(name='Titel', value=name)
                    album = str(lied.get_album())
                    album = album.replace(str(lied.get_artist()), '').replace(' - ', '')
                    embed.add_field(name='Artist', value=artist, inline=True)
                    footer = 'Album: ' + album + ' | ' + 'Duration: ' \
                            + str(minutes) + ':' + str(seconds) + ' | ' + 'Plays: ' + str(lied.get_playcount())
                    embed.set_footer(text=footer)
                    try:
                        genius = lyricsgenius.Genius(self.bot.LYRICS_KEY)
                        text = genius.search_song(title=str(lied.get_name()), artist=str(lied.get_artist()))
                        gesamter_text = str(text.lyrics).replace('EmbedShare URLCopyEmbedCopy', '')[0:5500]
                        while gesamter_text != "":
                            embed.add_field(name='Fortsetzung', value=(gesamter_text[0:1020]), inline=False)
                            gesamter_text = gesamter_text[1020:]
                    except Exception as e:
                        await ctx.channel.send(
                            'Irgendwas is schiefgelaufen lol. Vielleicht ist der Songtext länger als Discord zulässt?')
                        logger.error(f'Request from {ctx.author.name}: {e}')
                    await ctx.channel.send(embed=embed)
                    logger.info('Lyrics: Full gepostet für ' + ctx.author.name)
                except:
                    await ctx.channel.send('Dieser User hört gerade nix.')
                    logger.info('Lyrics: Full: User hört nichts für ' + ctx.author.name)
            elif method == 'link':
                try:
                    lied = user.get_now_playing()
                    seconds = (lied.get_duration() / 1000) % 60
                    seconds = int(seconds)
                    minutes = (lied.get_duration() / (1000 * 60)) % 60
                    minutes = int(minutes)
                    if seconds < 10:
                        seconds = "0" + str(seconds)

                    artisturl = 'https://www.last.fm/de/music/' + str(lied.get_artist()).replace(' ', '+')
                    songurl = artisturl + '/_/' + str(lied.get_name()).replace(' ', '+').replace('/', '%2F')
                    name = str('[' + str(lied.get_name()) + '](' + str(songurl) + ')')
                    artist = str('[' + str(lied.get_artist()) + '](' + str(artisturl) + ')')
                    embed = discord.Embed(title='', color=1917791)

                    if user.get_image() is not None:
                        embed.set_author(name=username, icon_url=user.get_image(),
                                        url='https://www.last.fm/user/' + username)
                    else:
                        embed.set_author(name=username, url='https://www.last.fm/user/' + username)

                    embed.set_thumbnail(url=str(lied.get_cover_image()))
                    embed.add_field(name='Titel', value=name)
                    album = str(lied.get_album())
                    album = album.replace(str(lied.get_artist()), '').replace(' - ', '')
                    embed.add_field(name='Artist', value=artist, inline=True)
                    footer = 'Album: ' + album + ' | ' + 'Duration: ' \
                            + str(minutes) + ':' + str(seconds) + ' | ' + 'Plays: ' + str(lied.get_playcount())
                    embed.set_footer(text=footer)
                    genius = Genius(self.bot.LYRICS_KEY)
                    song = genius.search_song(title=lied.get_title(), artist=lied.get_artist())
                    embed.add_field(name='Link', value=str('[' + str(lied) + '](' + str(song.url) + ')'),
                                    inline=False)

                    await ctx.channel.send(embed=embed)
                    logger.info('Lyrics: Link gepostet für ' + ctx.author.name)
                except Exception as e:
                    await ctx.channel.send('Dieser User hört gerade nix.')
                    logger.error(f'Request from {ctx.author.name}: {e}')

    @lyrics.error
    async def lyrics_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Format: "+lyrics (full/link) [USERNAME]"')


def setup(bot):
    bot.add_cog(Lyrics(bot))
