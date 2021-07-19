import time
import urllib.request
import pylast
import discord
from bs4 import BeautifulSoup
import lyricsgenius
from pyowm import OWM
import operator
import config

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
OMV_KEY = config.OMV_KEY
CLIENT_RUN = config.CLIENT_RUN
LYRICS_KEY = config.LYRICS_KEY

userdict = {}


class MyClient(discord.Client):

    @staticmethod
    async def on_ready():
        print("Hallo I bim omnline :^)")

    # Nachricht
    @staticmethod
    async def on_message(message):

        if message.author == client.user:
            return
        else:
            if message.content.startswith('+'):
                message.content = message.content[1:]
                if str(message.author) in userdict:
                    timealt = userdict[str(message.author)]
                else:
                    userdict[str(message.author)] = 10
                    timealt = userdict[str(message.author)]
                dauer = time.time() - timealt

                if dauer > 10:
                    await wiki(message)
                    await lyrics(message)
                    await bruh(message)
                    await wetter(message)


async def test(message):
    if message.content == "stop":
        liste = []
        blacklist = ['ich', 'das', 'die', 'ist', 'von', 'in', 'was', 'der', 'du', 'a', 'nicht', 'so', 'ja', 'zu', 'und'
            , 'mit', 'dann', 'es', 'auch', 'hier', 'aber', 'nur', 'da', 'man', 'ein', 'hat', 'mal', 'hab', 'schon'
            , 'wie', 'auf', 'hat', 'wird', 'wenn', 'is', 'mein', 'alles', 'ne', 'dass', 'bin', 'den', 'aus', 'mich',
                     'ok', 'für', 'mir', 'sind', 'eine', 'doch', 'warum', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '']
        blackliste = []
        dict = {}
        nummer = 25000
        zahl = 0
        messages = await message.channel.history(limit=nummer).flatten()
        for m in messages:
            if str(m.author) == str(message.author):
                zahl = zahl + 1
                liste = m.content.lower().split()
                for i in liste:
                    if i in blackliste:
                        pass
                    else:
                        if i in dict:
                            number = dict.get(i)
                            dict[str(i)] = number + 1
                        else:
                            dict[str(i)] = 1
        sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        embed = discord.Embed(title='Häufigste Wörter', color=0x00ff00)
        d = sorted_dict[:8]
        for i in d:
            embed.add_field(name='Wort', value=i[0])
            embed.add_field(name='Anzahl', value=i[1], inline=True)
            embed.add_field(name='Häufigkeit', value=(str(round((int(i[1]) / zahl) * 100))) + "%", inline=True)
        await message.channel.send(embed=embed)


async def bruh(message):
    if message.content == "bruh":
        userdict[str(message.author)] = time.time()
        await message.delete()
        embed = discord.Embed(title='Bruh', description='Bruh', url='https://www.youtube.com/watch?v=2ZIpFytCSVc',
                              color=0x00ff00)
        embed.set_footer(text='Bruh')
        embed.add_field(name='Bruh', value=message.author.mention + " sagt:")
        embed.set_image(url='https://i.imgur.com/qslkBXI.gif')
        embed.set_thumbnail(url='https://i.imgur.com/qslkBXI.gif')
        embed.set_author(name='Bruh', url='https://i.imgur.com/qslkBXI.gif')
        await message.channel.send(embed=embed)


async def wiki(message):
    try:
        if message.content.startswith('wiki'):
            userdict[str(message.author)] = time.time()
            wiki1 = message.content.replace('wiki ', '')
            wiki2 = wiki1.replace(' ', '_')
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
            await message.channel.send(embed=embed)
    except:
        if message.content.startswith('wiki'):
            userdict[str(message.author)] = time.time()
            wiki1 = message.content.replace('wiki ', '')
            wiki2 = wiki1.replace(' ', '_')
            wiki22 = wiki2.title()
            url = 'https://de.wikipedia.org/wiki/' + wiki22
            await message.channel.send('Jibtet nit. Probier doch mal selber: ' + url)


async def lyrics(message):
    if message.content.startswith('lyrics'):
        userdict[str(message.author)] = time.time()
        if message.content == 'lyrics':
            await message.channel.send('Format: "lyrics (now/recent/topartists/toptracks) [USERNAME]"')
            return
        if message.content == 'lyrics now' or message.content == 'lyrics recent':
            await message.channel.send('Ein Username wäre ganz hilfreich, retard.')
            return
        username = message.content.replace('lyrics now ', '').replace('lyrics recent ', '') \
            .replace('lyrics topartists ', '').replace('lyrics toptracks ', '').replace('lyrics topalbums ', '')
        wort = message.content.replace('lyrics ', '')
        try:
            network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
            user = network.get_user(username)
        except:
            await message.channel.send('User nit gefunden.')
            return
        if wort.startswith('now'):
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
                genius = lyricsgenius.Genius(LYRICS_KEY)
                text = genius.search_song(title=str(lied.get_name()), artist=str(lied.get_artist()))
                gesamter_text = str(text.lyrics).replace('EmbedShare URLCopyEmbedCopy', '')
                while gesamter_text != "":
                    embed.add_field(name='Fortsetzung', value=(gesamter_text[0:1020]), inline=False)
                    gesamter_text = gesamter_text[1020:]

                await message.channel.send(embed=embed)
            except:
                await message.channel.send('Dieser User hört gerade nix.')
        elif wort.startswith('recent'):
            liste = ''
            embed = discord.Embed(title='', color=1917791)

            for i in user.get_recent_tracks():
                liste = liste + str(i.track) + '\n'
            if liste == '':
                await message.channel.send('Keine kürzlich gespielten Lieder.')
            else:
                if user.get_image() is not None:
                    embed.set_author(name=username, icon_url=user.get_image(),
                                     url='https://www.last.fm/user/' + username)
                else:
                    embed.set_author(name=username, url='https://www.last.fm/user/' + username)
                embed.add_field(name='Kürzlich gespielte Lieder:', value=liste)
                await message.channel.send(embed=embed)
        elif wort.startswith('topartists'):
            try:
                liste = user.get_top_artists(username, limit=10)
            except:
                await message.channel.send('User nit gefunden.')
                return
            x = 1
            text = ''
            embed = discord.Embed(title='', color=1917791)
            for i in liste:
                text = text + '\n' + str(x) + ': ' + i.item.name + ' (Plays: ' + str(i.weight) + ')'
                x = x + 1

            if user.get_image() is not None:
                embed.set_author(name=username, icon_url=user.get_image(),
                                 url='https://www.last.fm/user/' + username)
            else:
                embed.set_author(name=username, url='https://www.last.fm/user/' + username)
            embed.add_field(name='Most played artists:', value=text)
            await message.channel.send(embed=embed)
        elif wort.startswith('toptracks'):
            try:
                liste = user.get_top_tracks(username, limit=10)
            except:
                await message.channel.send('User nit gefunden.')
                return
            x = 1
            text = ''
            embed = discord.Embed(title='', color=1917791)
            for i in liste:
                print(i.item)
                text = text + '\n' + str(x) + ': ' + str(i.item) + ' (Plays: ' + str(i.weight) + ')'
                x = x + 1

            if user.get_image() is not None:
                embed.set_author(name=username, icon_url=user.get_image(),
                                 url='https://www.last.fm/user/' + username)
            else:
                embed.set_author(name=username, url='https://www.last.fm/user/' + username)
            embed.add_field(name='Most played tracks:', value=text)
            await message.channel.send(embed=embed)
        elif wort.startswith('topalbums'):
            try:
                liste = user.get_top_albums(username, limit=10)
            except:
                await message.channel.send('User nit gefunden.')
                return
            x = 1
            text = ''
            embed = discord.Embed(title='', color=1917791)
            for i in liste:
                print(i.item)
                text = text + '\n' + str(x) + ': ' + str(i.item) + ' (Plays: ' + str(i.weight) + ')'
                x = x + 1
            if user.get_image() is not None:
                embed.set_author(name=username, icon_url=user.get_image(),
                                 url='https://www.last.fm/user/' + username)
            else:
                embed.set_author(name=username, url='https://www.last.fm/user/' + username)
            embed.add_field(name='Most played albums:', value=text)
            await message.channel.send(embed=embed)


async def wetter(message):
    owm = OWM(OMV_KEY)
    if message.content.startswith('wetter'):
        try:
            userdict[str(message.author)] = time.time()
            mgr = owm.weather_manager()
            place = message.content.replace('wetter ', '')
            observation = mgr.weather_at_place(place)
            wetter_neu = observation.weather
            embed = discord.Embed(title='Wetter in ' + place.title(), color=1917791)
            embed.set_author(name='Gott', icon_url='https://cdn.psychologytoday.com/sites'
                                                   '/default/files/field_blog_entry_images/God_the_Father.jpg')
            temp = wetter_neu.temperature('celsius')
            embed.add_field(name='Temperatur', value=str(round(temp['temp'], 1)) + '°C')
            embed.add_field(name='Luftfeuchtigkeit', value=str(wetter_neu.humidity) + '%', inline=True)
            embed.add_field(name='Status', value=wetter_neu.detailed_status, inline=False)
            await message.channel.send(embed=embed)
        except:
            await message.channel.send('Oopsie whoopsie, I did a fucky-wucky OwO.')


client = MyClient()
client.run(CLIENT_RUN)
