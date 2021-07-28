import time
import urllib.request
from datetime import datetime
import random

import pylast
import discord
import requests
from bs4 import BeautifulSoup
from lyricsgenius import Genius
import lyricsgenius
from pyowm import OWM
import config
import sqlite3
import asyncio
import urllib.request

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
OMV_KEY = config.OMV_KEY
CLIENT_RUN = config.CLIENT_RUN
LYRICS_KEY = config.LYRICS_KEY

# Wer das liest is blöd XD

userdict = {}

# connection
connection = sqlite3.connect('reminder-wishlist.db')
cursor = connection.cursor()

# table createn
try:
    creation1 = """CREATE TABLE IF NOT EXISTS
    reminders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, reminder_text TEXT, reminder_time INTEGER, channel INTEGER, message_id INTEGER)"""
    cursor.execute(creation1)
    creation2 = """CREATE TABLE IF NOT EXISTS wishlist(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, wishtext TEXT, ts TEXT)"""
    cursor.execute(creation2)
except:
    pass


class MyClient(discord.Client):

    @staticmethod
    async def on_ready():
        print("Hallo I bim omnline :^)")
        logging('========================Startup============================')
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
                    await git_gud(message)
                    await wishlist(message)
                    await show_wishlist(message)
                    await choose(message)
                    await benwach(message)
                    if message.author.id == 288413759117066241 or message.author.id == 156136437887008771:
                        await delete_wish(message)
                    if message.channel.id == 608746970340786282:
                        await lyrics(message)


async def choose(message):
    if message.content.startswith('choose'):
        try:
            userdict[str(message.author)] = time.time()
            new_message = message.content.replace('choose ', '').replace('choose', '')
            if new_message == "":
                await message.channel.send("Gib Optionen, Moruk")
            else:
                if '"' in new_message:
                    new_message_list = new_message.split('"')
                    cleared_list = []
                    for item in new_message_list:
                        if item == " " or item == "":
                            pass
                        else:
                            cleared_list.append(item)
                    if len(cleared_list) < 2:
                        await message.channel.send("Gib mehr als 1 Optionen, Moruk")
                        logging("ERROR: choose(): Zu wenig Optionen gegeben")
                    else:
                        choice = random.choice(cleared_list)
                        await message.channel.send(
                            "Oh magische Miesmuschel! Wie lautet deine Antwort? \n" + "**" + choice + "**")
                        logging("choose(): Antwort gepostet für: " + message.author.name)
                else:
                    new_message_list = new_message.split()
                    if len(new_message_list) < 2:
                        await message.channel.send("Gib mehr als 1 Optionen, Moruk")
                        logging("ERROR: choose(): Zu wenig Optionen gegeben")
                    else:
                        choice = random.choice(new_message_list)
                        await message.channel.send(
                            "Oh magische Miesmuschel! Wie lautet deine Antwort? \n" + "**" + choice + "**")
                        logging("choose(): Antwort gepostet für: " + message.author.name)

        except:
            await message.channel.send("Klappt nit lol 🤷")
            logging('ERROR: choose()')
    pass


async def reminder(message):
    unit_to_second = {"s": 1, "m": 60, "h": 60 * 60, "d": 60 * 60 * 24, "w": 60 * 60 * 24 * 7,
                      "mon": 60 * 60 * 24 * 7 * 30}

    if message.content.startswith('remindme'):
        # try:
        msg = message.content.replace("remindme ", '')

        userdict[str(message.author)] = time.time()  # die sollte global sein oder? #ja lol
        user_id = message.author.id
        channel = message.channel.id

        split_message = msg.split(" ")
        if split_message[0].isdigit():
            digits = split_message[0]
            unit = split_message[1]
            reminder_text = msg.split(" ", 2)[2]
        else:
            unit = split_message[0][-1]
            digits = split_message[0][:-1]
            reminder_text = msg.split(" ", 1)[1]

        reminder_time = round(time.time() + (float(int(digits) * int(unit_to_second[unit]))), 2)
        sql = "INSERT INTO reminders (user_id, reminder_text, reminder_time, channel, message_id) VALUES (?, ?, ?, ?, ?)"
        val = (user_id, reminder_text, reminder_time, channel, message.id)
        cursor.execute(sql, val)
        connection.commit()
        cursor.execute("SELECT id FROM reminders WHERE reminder_time=?", (reminder_time,))
        id = cursor.fetchall()[0][0]
        logging('Neuer Reminder in die DB gepusht: ' + str(id))
        channel = client.get_channel(channel)
        await message.add_reaction('\N{THUMBS UP SIGN}')
        logging('reminder(): Thumbs Up auf Nachricht reagiert')
        await wait_for_reminder(user_id, reminder_text, reminder_time, message, channel, id)
        '''except:
            await message.channel.send("Hm ne irgendwas gefällt mir daran nich. Nochmal? 🤷")
            logging('ERROR: reminder()')'''


def logging(text):
    with open('log.txt', 'a') as file:
        file.write(str(datetime.now().strftime("%Y/%m/%d, %H:%M:%S") + ': ' + text + '\n'))


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
            try:
                message = await channel.fetch_message(id=result[0][5])
            except:
                logging('Nächster Reminder geladen')
                await asyncio.sleep(reminder_time1 - time.time())
                await channel.send(
                    "<@{}>: Ich werde dich wissen lassen:\n**{}**".format(user_id, reminder_text))
                cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
                connection.commit()
                logging('Reminder gelöscht')
                await get_reminder_startup()
            await wait_for_reminder_startup(id, user_id, reminder_text, reminder_time1, channel_id, message)
    except:
        await message.channel.send(
            'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: get_reminder_startup()')
        logging('ERROR: get_reminder_startup()')


async def wait_for_reminder(user_id, reminder_text, reminder_time1, message, channel, id):
    try:
        if (reminder_time1 - time.time()) < 0:
            try:
                await message.reply(
                    "Ich werde dich wissen lassen:\n**{}**".format(reminder_text), mention_author=True)
                logging('Auf Reminder geantortet: ' + str(id))
            except:
                await channel.send(
                    "<@{}>: Ich werde dich wissen lassen:\n**{}**".format(user_id, reminder_text))
                logging('Auf Reminder geantortet: ' + str(id))
            cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
            connection.commit()
            logging('Reminder gelöscht: ' + str(id))
        else:
            logging('Nächster Reminder geladen: ' + str(id))
            await asyncio.sleep(reminder_time1 - time.time())
            try:
                await message.reply(
                    "Ich werde dich wissen lassen:\n**{}**".format(reminder_text), mention_author=True)
                logging('Auf Reminder geantortet: ' + str(id))
            except:
                await channel.send(
                    "<@{}>: Ich werde dich wissen lassen:\n**{}**".format(user_id, reminder_text))
                logging('Auf Reminder geantortet: ' + str(id))
            cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
            connection.commit()
            logging('Reminder gelöscht: ' + str(id))
    except:
        await message.channel.send('Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wait_for_reminder()')
        logging('ERROR: wait_for_reminder()')


async def wait_for_reminder_startup(id, user_id, reminder_text, reminder_time1, channel_id, message):
    try:
        channel = client.get_channel(channel_id)
        if (reminder_time1 - time.time()) < 0:
            await message.reply(
                "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
            logging('Auf Reminder geantortet: ' + str(id))
            cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
            connection.commit()
            logging('Reminder gelöscht: ' + str(id))
        else:
            logging('Nächster Reminder geladen: ' + str(id))
            await asyncio.sleep(reminder_time1 - time.time())
            await message.reply(
                "Ich werde dich wissen lassen:\n **{}**".format(reminder_text), mention_author=True)
            logging('Auf Reminder geantortet: ' + str(id))
            cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
            connection.commit()
            logging('Reminder gelöscht: ' + str(id))
        await get_reminder_startup()
    except:
        await channel.send('Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wait_for_reminder_startup()')
        logging('ERROR: wait_for_reminder_startup() von ' + message.author.name)


async def helpfunction(message):
    if message.content == "help":
        userdict[str(message.author)] = time.time()
        embed = discord.Embed(title='Help', description='Hier wird Ihnen geholfen!', color=0x00ff00)
        embed.add_field(name='+help', value="Öffnet das Hilfefenster", inline=False)
        embed.add_field(name='+lyrics', value="Format: +lyrics (full/link) [USERNAME]",
                        inline=False)
        embed.add_field(name='+wetter', value="Format: +wetter [ORTNAME]", inline=False)
        embed.add_field(name='+wiki', value="Format: +wiki [SUCHBEGRIFF]", inline=False)
        embed.add_field(name='+wishlist', value="Format: +wishlist [WUNSCH]", inline=False)
        embed.add_field(name='+showlist', value="Zeigt die Wunschliste an", inline=False)
        embed.add_field(name='+delwish', value="+delwish [ID] (nur für coole Menschen tho)", inline=False)
        embed.add_field(name='+remindme',
                        value="Format: +remindme [ZAHL][s/m/h/d/mon] [TEXT]",
                        inline=False)
        embed.add_field(name='+git', value="Poschded den link zum Github Repository", inline=False)
        embed.add_field(name='+benwach', value="Ben wach?", inline=False)
        embed.add_field(name='+choose',
                        value='+choose [Option 1] [Option 2] [...]\nBei mehreren Wörtern pro Option bitte jede Option in " " setzen.',
                        inline=False)
        embed.set_author(name='Gott', icon_url='https://cdn.psychologytoday.com/sites'
                                               '/default/files/field_blog_entry_images/God_the_Father.jpg')
        await message.channel.send(embed=embed)
        logging('Hilfefunktion ausgeführt von ' + message.author.name)


async def wiki(message):
    try:
        if message.content.startswith('wiki'):
            userdict[str(message.author)] = time.time()
            if message.content == 'wiki feet' or message.content == 'wikifeet':
                await message.channel.send(
                    'https://images.squarespace-cdn.com/content/v1/51323aa1e4b0b73e528cb71c/1567786369681-938Z512OX2Z03BDUGU62/Monty-Python-foot-1024x803.jpg')
                logging('Wikifeet gepostet für ' + message.author.name)
            else:
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
                logging('Wikiartikel gepostet für ' + message.author.name + ': ' + wiki1)
    except:
        if message.content.startswith('wiki'):
            userdict[str(message.author)] = time.time()
            wiki1 = message.content.replace('wiki ', '')
            wiki2 = wiki1.replace(' ', '_')
            wiki22 = wiki2.title()
            url = 'https://de.wikipedia.org/wiki/' + wiki22
            await message.channel.send('Jibtet nit. Probier doch mal selber: ' + url)
            logging('Wikiartikel nicht gefunden für ' + message.author.name + ': ' + wiki1)


async def lyrics(message):
    if message.content.startswith('lyrics'):
        userdict[str(message.author)] = time.time()
        if message.content == 'lyrics':
            await message.channel.send('Format: "+lyrics (full/link) [USERNAME]"')
            logging('Lyrics: Hilfe gepostet für ' + message.author.name)
            return
        if message.content == 'lyrics full' or message.content == 'lyrics link':
            await message.channel.send('Ein Username wäre ganz hilfreich, retard.')
            logging('Lyrics: kein Username angegeben von ' + message.author.name)
            return
        username = message.content.replace('lyrics full ', '').replace('lyrics link ', '')
        wort = message.content.replace('lyrics ', '')
        try:
            network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
            user = network.get_user(username)
        except:
            await message.channel.send('User nit gefunden.')
            logging('Lyrics: User nicht gefunden für ' + message.author.name)
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
                    logging('ERROR: Lyrics Full von ' + message.author.name)

                await message.channel.send(embed=embed)
                logging('Lyrics: Full gepostet für ' + message.author.name)
            except:
                await message.channel.send('Dieser User hört gerade nix.')
                logging('Lyrics: Full: User hört nichts für ' + message.author.name)
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
                logging('Lyrics: Link gepostet für ' + message.author.name)
            except:
                await message.channel.send('Dieser User hört gerade nix.')
                logging('ERROR: Lyrics: Link: User hört nichts von ' + message.author.name)


'''async def wetter(message):
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
            logging('Wetter gepostet für ' + message.author.name + ': ' + place)
        except:
            await message.channel.send(
                'Wetter schmetter, sag ich schon immer.')
            logging('ERROR: Wetter für ' + message.author.name)'''


async def wetter(message):
    if message.content.startswith('wetter '):
        try:
            userdict[str(message.author)] = time.time()
            place = message.content.replace('wetter ', '').replace(' ', '-')
            '''url = 'https://wttr.in/{}'.format(place) + "?n&T&2&lang=de"
            res = requests.get(url)
            await message.channel.send(
                "```" + res.text.replace("Folgen Sie https://twitter.com/igor_chubin für wttr.in Updates", "") + "```")'''
            url_png = 'https://de.wttr.in/{}'.format(place) + "_m" + ".png"
            urllib.request.urlretrieve(url_png,
                                       "wetter.png")

            await message.channel.send(file=discord.File(r'wetter.png'))
            logging('Wetter gepostet für ' + message.author.name + ': ' + place)
        except:
            await message.channel.send(
                'Wetter schmetter, sag ich schon immer.')
            logging('ERROR: Wetter für ' + message.author.name)


async def git_gud(message):
    if message.content == 'git':
        try:
            await message.channel.send("https://github.com/Zicklaa/Zicklaa-Bot")
            logging('Git Link gepostet für ' + message.author.name)
        except:
            await message.channel.send(
                'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: git_gud()')
            logging('ERROR: Git von ' + message.author.name)


async def wishlist(message):
    try:
        if message.content.startswith('wishlist'):
            userdict[str(message.author)] = time.time()
            wishtext = message.content[9:]
            if len(wishtext) < 250:
                user_id = message.author.id
                ts = datetime.now().strftime("%d-%b-%Y | %H:%M:%S")
                if not wishtext:
                    await message.channel.send(
                        'Leere Wünsche: Name meiner Autobiographie.')
                    logging('Wishlist: Leerer Wunsch von ' + message.author.name)
                else:
                    sql = "INSERT INTO wishlist (user_id, wishtext, ts) VALUES (?, ?, ?)"
                    val = (user_id, wishtext, ts)
                    cursor.execute(sql, val)
                    connection.commit()

                    await message.add_reaction('\N{THUMBS UP SIGN}')
                    logging('Wishlist: neuer Wunsch + Reaktion')
            else:
                await message.channel.send(
                    'Wunsch zu lang, maximal 250 Chars.')
                logging('Wishlist: Wunsch zu lang von ' + message.author.name)
    except:
        await message.channel.send(
            'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wishlist()')
        logging('ERROR: Wishlist von ' + message.author.name)


async def show_wishlist(message):
    try:
        if message.content == 'showlist':
            userdict[str(message.author)] = time.time()
            cursor.execute("SELECT * FROM wishlist")
            wishes = cursor.fetchall()
            if not wishes:
                await message.channel.send(
                    'Ihr seid wunschlos glücklich :3')
                logging('Wishlist: Leer für ' + message.author.name)
            else:
                all_wishes = 'Folgendes wünscht ihr euch: \n\n'
                x = 1
                for wish in wishes:
                    all_wishes = all_wishes + 'ID: ' + str(wish[0]) + ': ' + '\n'
                    all_wishes = all_wishes + '**' + wish[2] + '**' + '\n'
                    all_wishes = all_wishes + '<@' + str(wish[1]) + '>' + ' (' + wish[
                        3] + ')' + '\n' + '\n'
                    x = x + 1
                    if len(all_wishes) > 1999:
                        await message.channel.send(all_wishes)
                        await message.channel.send("Es fehlen Wünsche da Discord Zeichenlimit lol")
                        logging('Wishlist: Inkomplette Liste gepostet für ' + message.author.name)
                        break
                await message.channel.send(all_wishes)
                logging('Wishlist: Liste gepostet für ' + message.author.name)
    except:
        await message.channel.send(
            'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: show_wishlist()')
        logging('ERROR: Wishlist von ' + message.author.name)


async def delete_wish(message):
    if message.content.startswith('delwish '):
        userdict[str(message.author)] = time.time()
        wishtext = message.content.split()
        if len(wishtext) < 2:
            await message.channel.send(
                'Gib eine ID an oder so, Lan')
            logging('delete_wish: Keine ID von ' + message.author.name)
        else:
            try:
                id = int(wishtext[1])
                cursor.execute("SELECT * FROM wishlist WHERE id=?", (id,))
                wish = cursor.fetchall()
                if not wish:
                    await message.channel.send(
                        'Ein Wunsch mit der ID gibts nedde')
                    logging('delete_wish: Wish beim Löschen nicht gefunden')
                else:
                    cursor.execute("DELETE FROM wishlist WHERE id=?", (id,))
                    connection.commit()
                    await message.add_reaction('\N{THUMBS UP SIGN}')
                    logging('delete_wish: Wish gelöscht mit der ID: ' + str(id))
            except:
                await message.channel.send(
                    'Irgendwas stimmt mit der ID nicht, Mois')
                logging('ERROR: delete_wish: Fehler bei Eingabe der ID')


async def benwach(message):
    try:
        if message.content == 'benwach':
            current_hour = datetime.now().hour
            if 0 <= current_hour < 6:
                await message.reply("Ben ist wahrscheinlich grad wach :))")
            elif 6 <= current_hour < 14:
                await message.reply("Spinnst du? Hast du mal auf die Uhr gekuckt?")
            elif 14 <= current_hour < 24:
                await message.reply("Ben ist wahrscheinlich grad wach :))")
    except:
        await message.channel.send(
            'Irgendwas stimmt nicht, Mois')
        logging('ERROR: benwach: Fehler')


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
