import time
import urllib.request
import pylast
import discord
from bs4 import BeautifulSoup
from lyricsgenius import Genius
import lyricsgenius
from pyowm import OWM
import config
import sqlite3
import asyncio

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
OMV_KEY = config.OMV_KEY
CLIENT_RUN = config.CLIENT_RUN
LYRICS_KEY = config.LYRICS_KEY

# Wer das liest ist blöd XD

userdict = {}

# connection
connection = sqlite3.connect('reminder.db')
cursor = connection.cursor()

# table createn
try:
    creation = """CREATE TABLE IF NOT EXISTS
    reminders(id INTEGER PRIMARY KEY, user_id INTEGER, reminder_text TEXT, reminder_time INTEGER, channel INTEGER, message_id INTEGER)"""
    cursor.execute(creation)
except:
    pass


class MyClient(discord.Client):

    @staticmethod
    async def on_ready():
        print("Hallo I bim omnline :^)")
        await get_reminder_startup()

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

                if dauer > 5:
                    await wiki(message)
                    await wetter(message)
                    await helpfunction(message)
                    await reminder(message)
                    #if message.channel.id == 608746970340786282:
                    await lyrics(message)


async def reminder(message):
    if "remindme" in message.content:
        try:
            userdict[str(message.author)] = time.time()
            user_id = message.author.id
            split_message = message.content.split(" ")
            if split_message[2] == "seconds" or split_message[2] == "s":
                reminder_time1 = round(time.time() + float(split_message[1]), 2)
            elif split_message[2] == "minutes" or split_message[2] == "m":
                reminder_time1 = round(time.time() + (float(split_message[1]) * 60), 2)
            elif split_message[2] == "hours" or split_message[2] == "h":
                reminder_time1 = round(time.time() + (int(split_message[1]) * 3600), 2)
            elif split_message[2] == "days" or split_message[2] == "d":
                reminder_time1 = round(time.time() + (int(split_message[1]) * 86400), 2)
            elif split_message[2] == "weeks" or split_message[2] == "w":
                reminder_time1 = round(time.time() + (int(split_message[1]) * 604800), 2)
            elif split_message[2] == "months":
                reminder_time1 = round(time.time() + (int(split_message[1]) * 2678400), 2)
            del split_message[:3]
            reminder_text = " ".join(split_message)
            channel = message.channel.id
            sql = "INSERT INTO reminders (user_id, reminder_text, reminder_time, channel, message_id) VALUES (?, ?, ?, ?, ?)"
            val = (user_id, reminder_text, reminder_time1, channel, message.id)
            cursor.execute(sql, val)
            connection.commit()
            await message.add_reaction('\N{THUMBS UP SIGN}')
            await wait_for_reminder(reminder_text, reminder_time1, message)
        except:
            await message.channel.send("Hm ne irgendwas gefällt mir daran nich. Nochmal? 🤷")


async def get_reminder_startup():
    try:
        cursor.execute("SELECT * FROM reminders ORDER BY reminder_time ASC LIMIT 1")
        result = cursor.fetchall()
        if result:
            id = result[0][0]
            user_id = result[0][1]
            reminder_text = result[0][2]
            reminder_time1 = result[0][3]
            channel_id = result[0][4]
            channel = client.get_channel(channel_id)
            message = await channel.fetch_message(id=result[0][5])
            await wait_for_reminder_startup(id, user_id, reminder_text, reminder_time1, channel_id, message)
    except:
        await message.channel.send(
            'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: get_reminder_startup()')


async def wait_for_reminder(reminder_text, reminder_time1, message):
    try:
        if (reminder_time1 - time.time()) < 0:
            await message.reply(
                "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
            cursor.execute("DELETE FROM reminders WHERE reminder_time=?", (reminder_time1,))
            connection.commit()
        else:
            await asyncio.sleep(reminder_time1 - time.time())
            await message.reply(
                "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
            cursor.execute("DELETE FROM reminders WHERE reminder_time=?", (reminder_time1,))
            connection.commit()
    except:
        await message.channel.send('Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wait_for_reminder()')


async def wait_for_reminder_startup(id, user_id, reminder_text, reminder_time1, channel_id, message):
    try:
        channel = client.get_channel(channel_id)
        if (reminder_time1 - time.time()) < 0:
            await message.reply(
                "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
            cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
            connection.commit()
        else:
            await asyncio.sleep(reminder_time1 - time.time())
            await message.reply(
                "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
            cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
            connection.commit()
        await get_reminder_startup()
    except:
        await channel.send('Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wait_for_reminder_startup()')


async def helpfunction(message):
    if message.content == "help":
        userdict[str(message.author)] = time.time()
        embed = discord.Embed(title='Help', description='Hier wird Ihnen geholfen!', color=0x00ff00)
        embed.add_field(name='+help', value="Öffnet das Hilfefenster ", inline=False)
        embed.add_field(name='+lyrics', value="Format: +lyrics (full/link) [USERNAME]",
                        inline=False)
        embed.add_field(name='+wetter', value="Format: +wetter [ORTNAME]", inline=False)
        embed.add_field(name='+wiki', value="Format: +wiki [SUCHBEGRIFF]", inline=False)
        embed.add_field(name='+remindme',
                        value="Format: +remindme [ZAHL] [seconds or s/minutes or m/hours or h/days or d/months] [TEXT]",
                        inline=False)
        embed.set_author(name='Gott', icon_url='https://cdn.psychologytoday.com/sites'
                                               '/default/files/field_blog_entry_images/God_the_Father.jpg')
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
            await message.channel.send('Format: "+lyrics (full/link) [USERNAME]"')
            return
        if message.content == 'lyrics full' or message.content == 'lyrics link':
            await message.channel.send('Ein Username wäre ganz hilfreich, retard.')
            return
        username = message.content.replace('lyrics full ', '').replace('lyrics link ', '')
        wort = message.content.replace('lyrics ', '')
        try:
            network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
            user = network.get_user(username)
        except:
            await message.channel.send('User nit gefunden.')
            return
        if wort.startswith('full'):
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
                    genius = lyricsgenius.Genius(LYRICS_KEY)
                    text = genius.search_song(title=str(lied.get_name()), artist=str(lied.get_artist()))
                    gesamter_text = str(text.lyrics).replace('EmbedShare URLCopyEmbedCopy', '')[0:5500]
                    while gesamter_text != "":
                        embed.add_field(name='Fortsetzung', value=(gesamter_text[0:1020]), inline=False)
                        gesamter_text = gesamter_text[1020:]
                except:
                    await message.channel.send(
                        'Irgendwas is schiefgelaufen lol. Vielleicht ist der Songtext länger als Discord zulässt?')

                await message.channel.send(embed=embed)
            except:
                await message.channel.send('Dieser User hört gerade nix.')
        elif wort.startswith('link'):
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
                genius = Genius(LYRICS_KEY)
                song = genius.search_song(title=lied.get_title(), artist=lied.get_artist())
                embed.add_field(name='Link', value=str('[' + str(lied) + '](' + str(song.url) + ')'),
                                inline=False)

                await message.channel.send(embed=embed)
            except:
                await message.channel.send('Dieser User hört gerade nix.')


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
            await message.channel.send(
                'Wetter schmetter, sag ich schon immer.')


''' def test(message):
         if message.content == "stop":
             liste = []
             blacklist = ['ich', 'das', 'die', 'ist', 'von', 'in', 'was', 'der', 'du', 'a', 'nicht', 'so', 'ja',
                          'zu', 'und'
                 , 'mit', 'dann', 'es', 'auch', 'hier', 'aber', 'nur', 'da', 'man', 'ein', 'hat', 'mal', 'hab',
                          'schon'
                 , 'wie', 'auf', 'hat', 'wird', 'wenn', 'is', 'mein', 'alles', 'ne', 'dass', 'bin', 'den', 'aus',
                          'mich',
                          'ok', 'für', 'mir', 'sind', 'eine', 'doch', 'warum', '', '', '', '', '', '', '', '', '',
                          '', '',
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
             await message.channel.send(embed=embed)'''

'''async def bruh(message):
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
        await message.channel.send(embed=embed)'''

client = MyClient()
client.run(CLIENT_RUN)
