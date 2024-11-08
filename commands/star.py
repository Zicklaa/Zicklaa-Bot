from datetime import datetime, timezone
import logging
import os
import discord
from discord.ext import commands
from discord.raw_models import RawReactionActionEvent
from collections.abc import Sequence
from dateutil import tz
import re
from config import globalPfad
import pytz


logger = logging.getLogger("ZicklaaBot.Star")

post_channel_id = 981543834129428560  # Mainchannel
#post_channel_id = 567411189336768532  # Testchannel
threshold = 5
ext_list = [
    "3g2",
    "3gp",
    "amv",
    "asf",
    "avi",
    "gifv",
    "m4p",
    "m4v",
    "mov",
    "mp2",
    "mp4",
    "mpeg",
    "mpg",
    "webm",
]
path = globalPfad + "LustigeBildchen/"


class Star(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.cursor = db.cursor()

    def parse_raw_reaction_event(self, payload: RawReactionActionEvent):
        return payload.message_id, payload.channel_id, payload.emoji, payload.user_id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        message_id, channel_id, emoji, user_id = self.parse_raw_reaction_event(payload)
        if str(emoji) == "⭐" and int(channel_id) != post_channel_id:
            try:
                cache_msg = discord.utils.get(self.bot.cached_messages, id=message_id)
                reactions = cache_msg.reactions
                star_dict = {}
                for reaction in reactions:
                    star_dict.update({reaction.emoji: reaction.count})
                if int(star_dict["⭐"]) == threshold:
                    try:
                        self.cursor.row_factory = lambda cursor, row: row[0]
                        posted_stars = self.cursor.execute(
                            "SELECT message_id FROM stars"
                        ).fetchall()
                    except Exception as e:
                        logger.error(f"Noch keine geposteten Stars: {e}")
                    if message_id not in posted_stars:
                        channel = self.bot.get_channel(channel_id)
                        message = await channel.fetch_message(message_id)
                        embed = discord.Embed(
                            title="", description=message.content, color=0xFFEA00
                        )
                        time = (
                            pytz.utc.localize(message.created_at).astimezone(tz.tzlocal())
                        ).strftime("%d.%m.%Y, %H:%M:%S")
                        if message.attachments:
                            if any(ext in message.attachments[0].url for ext in ext_list):
                                embed.add_field(
                                    name="Link zum Video:",
                                    value="[Video](" + message.attachments[0].url + ")",
                                    inline=True,
                                )
                                dateiEndung = ".mp4"
                            else:
                                embed.set_image(url=str(message.attachments[0].url))
                                dateiEndung = ".png"
                            try:
                                for i, attachements in enumerate(message.attachments):
                                    filename = (
                                        path
                                        + "STERNBRETT_"
                                        + str(message_id)
                                        + "_"
                                        + str(i)
                                        + dateiEndung
                                    )
                                    await attachements.save(filename)
                            except:
                                logger.error(f"Star Error beim LTB speichern: {e}")

                        embed.add_field(
                            name="Link zur Nachricht:",
                            value="[Nachricht](" + message.jump_url + ")",
                            inline=True,
                        )
                        embed.set_author(
                            name=message.author.name,
                            icon_url=message.author.avatar_url,
                            url=message.jump_url,
                        )
                        embed.set_footer(text=time + " | #" + message.channel.name)
                        channel = self.bot.get_channel(post_channel_id)
                        star_message = await channel.send(embed=embed)
                        await star_message.add_reaction("⭐")
                        try:
                            sql = "INSERT INTO stars (message_id) VALUES (?)"
                            val = (int(message_id),)
                            self.cursor.execute(sql, val)
                            self.db.commit()
                        except Exception as e:
                            logger.error(f"Star Error beim DB pushen: {e}")

                        logger.info("Star gepostet")
            except Exception as e:
                logger.error(f"Star Error: {e}")

    @commands.command()
    async def star(self, ctx, link):
        try:
            if int(ctx.author.id) == 288413759117066241:
                if link:
                    try:
                        link = link.split("/")
                        channel_id = int(link[5])
                        msg_id = int(link[6])
                        channel = self.bot.get_channel(channel_id)
                        message = await channel.fetch_message(msg_id)
                        try:
                            self.cursor.row_factory = lambda cursor, row: row[0]
                            posted_stars = self.cursor.execute(
                                "SELECT message_id FROM stars"
                            ).fetchall()
                        except Exception as e:
                            logger.error(f"Noch keine geposteten Stars: {e}")
                        if msg_id not in posted_stars:
                            channel = self.bot.get_channel(channel_id)
                            message = await channel.fetch_message(msg_id)
                            embed = discord.Embed(
                                title="", description=message.content, color=0xFFEA00
                            )
                            time = (
                                pytz.utc.localize(message.created_at).astimezone(
                                    tz.tzlocal()
                                )
                            ).strftime("%d.%m.%Y, %H:%M:%S")
                            if message.attachments:
                                if any(
                                    ext in message.attachments[0].url
                                    for ext in ext_list
                                ):
                                    embed.add_field(
                                        name="Link zum Video:",
                                        value="[Video]("
                                        + message.attachments[0].url
                                        + ")",
                                        inline=True,
                                    )
                                else:
                                    embed.set_image(url=str(message.attachments[0].url))
                            embed.add_field(
                                name="Link zur Nachricht:",
                                value="[Nachricht](" + message.jump_url + ")",
                                inline=True,
                            )
                            embed.set_author(
                                name=message.author.name,
                                icon_url=message.author.avatar_url,
                                url=message.jump_url,
                            )
                            embed.set_footer(text=time + " | #" + message.channel.name)
                            channel = self.bot.get_channel(post_channel_id)
                            star_message = await channel.send(embed=embed)
                            await star_message.add_reaction("⭐")
                            await message.add_reaction("✅")
                            try:
                                sql = "INSERT INTO stars (message_id) VALUES (?)"
                                val = (int(msg_id),)
                                self.cursor.execute(sql, val)
                                self.db.commit()
                            except Exception as e:
                                await message.add_reaction("❌")
                                logger.error(f"Star Error beim DB pushen: {e}")

                            logger.info("Star gepostet")
                    except Exception as e:
                        await ctx.reply("Link br0ke 🤷")
                        await ctx.add_reaction("❌")
                        logger.error(f"Star from {ctx.author.name}: {e}")
                else:
                    await ctx.reply(
                        "Wie soll ich das sternen wenn du nichtmal ne Link gibst, du Mong?"
                    )
                    await ctx.add_reaction("❌")
                    logger.info("Star(): Kein Link gegeben von: " + ctx.author.name)
            else:
                await ctx.add_reaction("❌")
                await ctx.reply("Das ist VERBOTEN!!")
                logger.info("Star(): Kein Admin von: " + ctx.author.name)
        except Exception as e:
            logger.error(f"Star from {ctx.author.name}: {e}")

    '''
    @commands.command()
    async def topstar1(self, ctx):
        # Fixed channel ID
        start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        url_regex = r'https?://\S+'
        channel_id = 981543834129428560  # Replace with your channel ID
        channel = self.bot.get_channel(channel_id)
        all_urls_list = []
        if not channel:
            print("Channel not found.")
            return

        try:
            # Fetch messages from the channel
            async for message in channel.history(limit=600):  # Adjust limit as needed
                # Check if the message is within the date range
                message_created_at = message.created_at.replace(tzinfo=timezone.utc)

                if start_date <= message_created_at <= end_date:
                    for embed in message.embeds:
                        for field in embed.fields:
                        # Check both name and value of the field for URLs
                            urls = re.findall(url_regex, field.name)
                            urls.extend(re.findall(url_regex, field.value))

                            for url in urls:
                                if "https://discord.com" in url:
                                    all_urls_list.append(url)
        except discord.Forbidden:
            print("I don't have permission to access messages in this channel.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        print(all_urls_list)

    @commands.command()
    async def topstar2(self, ctx):
        urls = ['https://discord.com/channels/122739462210846721/122739462210846721/1186711812679409714)', 'https://discord.com/channels/122739462210846721/122739462210846721/1186378764209361057)', 'https://discord.com/channels/122739462210846721/122739462210846721/1185620789890928731)', 'https://discord.com/channels/122739462210846721/122739462210846721/1185147715743658075)', 'https://discord.com/channels/122739462210846721/122739462210846721/1185129073782050836)', 'https://discord.com/channels/122739462210846721/122739462210846721/1183912013555048569)', 'https://discord.com/channels/122739462210846721/122739462210846721/1183483577195835392)', 'https://discord.com/channels/122739462210846721/122739462210846721/1183197680332197968)', 'https://discord.com/channels/122739462210846721/122739462210846721/1182845270615134218)', 'https://discord.com/channels/122739462210846721/122739462210846721/1182840407894270003)', 'https://discord.com/channels/122739462210846721/608785121449082898/1182736453210480760)', 'https://discord.com/channels/122739462210846721/122739462210846721/1182271187330551859)', 'https://discord.com/channels/122739462210846721/122739462210846721/1181880375413313537)', 'https://discord.com/channels/122739462210846721/860154286141997056/1180100017214738433)', 'https://discord.com/channels/122739462210846721/122739462210846721/1179792339552706744)', 'https://discord.com/channels/122739462210846721/608746970340786282/1179558334811095140)', 'https://discord.com/channels/122739462210846721/122739462210846721/956340185459720242)', 'https://discord.com/channels/122739462210846721/122739462210846721/1179156256942997685)', 'https://discord.com/channels/122739462210846721/122739462210846721/1179052572573716521)', 'https://discord.com/channels/122739462210846721/122739462210846721/1177727411530510366)', 'https://discord.com/channels/122739462210846721/122739462210846721/1177309021020106813)', 'https://discord.com/channels/122739462210846721/528742785935998979/1176976023972229210)', 'https://discord.com/channels/122739462210846721/608746970340786282/1176989269429067866)', 'https://discord.com/channels/122739462210846721/122739462210846721/1176140646743019561)', 'https://discord.com/channels/122739462210846721/675448334089060409/1175894655112585256)', 'https://discord.com/channels/122739462210846721/608746970340786282/1175547454100348970)', 'https://discord.com/channels/122739462210846721/122739462210846721/1175466611105333298)', 'https://discord.com/channels/122739462210846721/608785121449082898/1174792406995058688)', 'https://discord.com/channels/122739462210846721/122739462210846721/1174746087651807333)', 'https://discord.com/channels/122739462210846721/122739462210846721/1173945414832107540)', 'https://discord.com/channels/122739462210846721/122739462210846721/1172614344505303150)', 'https://discord.com/channels/122739462210846721/608746838333587456/1172211476493250611)', 'https://discord.com/channels/122739462210846721/675448334089060409/1171934644447498250)', 'https://discord.com/channels/122739462210846721/860154286141997056/1171834034997973022)', 'https://discord.com/channels/122739462210846721/122739462210846721/1171810138512953364)', 'https://discord.com/channels/122739462210846721/122739462210846721/1169746264141865060)', 'https://discord.com/channels/122739462210846721/608785121449082898/1169668241312976997)', 'https://discord.com/channels/122739462210846721/122739462210846721/1169606469734375494)', 'https://discord.com/channels/122739462210846721/122739462210846721/1168865355020632144)', 'https://discord.com/channels/122739462210846721/122739462210846721/1168628129259077663)', 'https://discord.com/channels/122739462210846721/122739462210846721/1168612325318742117)', 'https://discord.com/channels/122739462210846721/122739462210846721/1168543812579233855)', 'https://discord.com/channels/122739462210846721/122739462210846721/1168537411224088616)', 'https://discord.com/channels/122739462210846721/122739462210846721/1167146657457131651)', 'https://discord.com/channels/122739462210846721/528742785935998979/1166361925458853961)', 'https://discord.com/channels/122739462210846721/122739462210846721/1165968296760332359)', 'https://discord.com/channels/122739462210846721/122739462210846721/1164251455763513434)', 'https://discord.com/channels/122739462210846721/608746838333587456/1163757709817020447)', 'https://discord.com/channels/122739462210846721/122739462210846721/1163553550459224134)', 'https://discord.com/channels/122739462210846721/122739462210846721/1163442209950023701)', 'https://discord.com/channels/122739462210846721/122739462210846721/1163440931375157359)', 'https://discord.com/channels/122739462210846721/122739462210846721/1162633424205516950)', 'https://discord.com/channels/122739462210846721/122739462210846721/1162294229553401896)', 'https://discord.com/channels/122739462210846721/122739462210846721/1162283864329293824)', 'https://discord.com/channels/122739462210846721/122739462210846721/1162021556633997322)', 'https://discord.com/channels/122739462210846721/122739462210846721/1161720532140572772)', 'https://discord.com/channels/122739462210846721/122739462210846721/1161674967893672037)', 'https://discord.com/channels/122739462210846721/122739462210846721/1161673128859144354)', 'https://discord.com/channels/122739462210846721/122739462210846721/1161670039053811752)', 'https://discord.com/channels/122739462210846721/122739462210846721/1161390301559132240)', 'https://discord.com/channels/122739462210846721/122739462210846721/1160883264710516867)', 'https://discord.com/channels/122739462210846721/528742785935998979/1160595248972570645)', 'https://discord.com/channels/122739462210846721/122739462210846721/1160159844347691078)', 'https://discord.com/channels/122739462210846721/122739462210846721/1159882669610520606)', 'https://discord.com/channels/122739462210846721/122739462210846721/1159134043665858560)', 'https://discord.com/channels/122739462210846721/122739462210846721/1158354766167031808)', 'https://discord.com/channels/122739462210846721/122739462210846721/1157393272331841617)', 'https://discord.com/channels/122739462210846721/122739462210846721/1157331660271001681)', 'https://discord.com/channels/122739462210846721/122739462210846721/1156263116942880810)', 'https://discord.com/channels/122739462210846721/122739462210846721/1155613696572272680)', 'https://discord.com/channels/122739462210846721/122739462210846721/1155610120496107541)', 'https://discord.com/channels/122739462210846721/122739462210846721/1153052357807046767)', 'https://discord.com/channels/122739462210846721/122739462210846721/1153033801895776387)', 'https://discord.com/channels/122739462210846721/122739462210846721/1152627354435342356)', 'https://discord.com/channels/122739462210846721/528742785935998979/1152274349282312283)', 'https://discord.com/channels/122739462210846721/608746838333587456/1151132996687110165)', 'https://discord.com/channels/122739462210846721/122739462210846721/1151131622901559307)', 'https://discord.com/channels/122739462210846721/608746970340786282/1150840991041994773)', 'https://discord.com/channels/122739462210846721/122739462210846721/1149080473285447700)', 'https://discord.com/channels/122739462210846721/122739462210846721/1148928330104586320)', 'https://discord.com/channels/122739462210846721/122739462210846721/1148379643330707486)', 'https://discord.com/channels/122739462210846721/122739462210846721/1148340362209939580)', 'https://discord.com/channels/122739462210846721/122739462210846721/1148199251197825044)', 'https://discord.com/channels/122739462210846721/528742785935998979/1148139286428917760)', 'https://discord.com/channels/122739462210846721/608746838333587456/1147942157907402863)', 'https://discord.com/channels/122739462210846721/122739462210846721/1147939178961703002)', 'https://discord.com/channels/122739462210846721/122739462210846721/1146774172937236682)', 'https://discord.com/channels/122739462210846721/122739462210846721/1146528176189739151)', 'https://discord.com/channels/122739462210846721/122739462210846721/1146450250287022124)', 'https://discord.com/channels/122739462210846721/122739462210846721/1146450232910033006)', 'https://discord.com/channels/122739462210846721/122739462210846721/1146450224596930713)', 'https://discord.com/channels/122739462210846721/122739462210846721/1146424587815489698)', 'https://discord.com/channels/122739462210846721/122739462210846721/1146368802834108550)', 'https://discord.com/channels/122739462210846721/122739462210846721/1145968387034452068)', 'https://discord.com/channels/122739462210846721/122739462210846721/1144321584396509236)', 'https://discord.com/channels/122739462210846721/122739462210846721/1144319704165519481)', 'https://discord.com/channels/122739462210846721/122739462210846721/1144222999193604126)', 'https://discord.com/channels/122739462210846721/122739462210846721/1143989564294320258)', 'https://discord.com/channels/122739462210846721/122739462210846721/1141378214812459079)', 'https://discord.com/channels/122739462210846721/122739462210846721/1141363404032987258)', 'https://discord.com/channels/122739462210846721/122739462210846721/1141355868059877377)', 'https://discord.com/channels/122739462210846721/122739462210846721/1141344204052770956)', 'https://discord.com/channels/122739462210846721/122739462210846721/1140629635642691695)', 'https://discord.com/channels/122739462210846721/122739462210846721/1139214709913030727)', 'https://discord.com/channels/122739462210846721/122739462210846721/1139212825257058314)', 'https://discord.com/channels/122739462210846721/860154286141997056/1137795248026833047)', 'https://discord.com/channels/122739462210846721/528742785935998979/1136977897589063731)', 'https://discord.com/channels/122739462210846721/528742785935998979/1136774256995340370)', 'https://discord.com/channels/122739462210846721/122739462210846721/1136764605260116200)', 'https://discord.com/channels/122739462210846721/122739462210846721/1136660675977035808)', 'https://discord.com/channels/122739462210846721/122739462210846721/1136626083568046182)', 'https://discord.com/channels/122739462210846721/122739462210846721/1136611398793834619)', 'https://discord.com/channels/122739462210846721/122739462210846721/1136587068823322715)', 'https://discord.com/channels/122739462210846721/122739462210846721/1135540950303780884)', 'https://discord.com/channels/122739462210846721/608746838333587456/1135106440017748030)', 'https://discord.com/channels/122739462210846721/122739462210846721/1135110730807529542)', 'https://discord.com/channels/122739462210846721/528742785935998979/1134844145538707597)', 'https://discord.com/channels/122739462210846721/528742785935998979/1134802142130098268)', 'https://discord.com/channels/122739462210846721/122739462210846721/1134771049054089269)', 'https://discord.com/channels/122739462210846721/860154286141997056/1134527747989983262)', 'https://discord.com/channels/122739462210846721/122739462210846721/1134462715834937374)', 'https://discord.com/channels/122739462210846721/122739462210846721/1134421590084427777)', 'https://discord.com/channels/122739462210846721/122739462210846721/1133727969437814865)', 'https://discord.com/channels/122739462210846721/122739462210846721/1133490435050963134)', 'https://discord.com/channels/122739462210846721/122739462210846721/1133347207219777536)', 'https://discord.com/channels/122739462210846721/122739462210846721/1133145918640771072)', 'https://discord.com/channels/122739462210846721/122739462210846721/1132967602705145876)', 'https://discord.com/channels/122739462210846721/528742785935998979/1131658887418875926)', 'https://discord.com/channels/122739462210846721/122739462210846721/1131488257859911810)', 'https://discord.com/channels/122739462210846721/122739462210846721/1130550315092025475)', 'https://discord.com/channels/122739462210846721/122739462210846721/1130546668186644551)', 'https://discord.com/channels/122739462210846721/122739462210846721/1129329300655583313)', 'https://discord.com/channels/122739462210846721/122739462210846721/1129145831832961114)', 'https://discord.com/channels/122739462210846721/122739462210846721/1129144491681525761)', 'https://discord.com/channels/122739462210846721/122739462210846721/1129058272771592213)', 'https://discord.com/channels/122739462210846721/122739462210846721/1129002783765442670)', 'https://discord.com/channels/122739462210846721/122739462210846721/1128761890923876443)', 'https://discord.com/channels/122739462210846721/122739462210846721/1128675548726558850)', 'https://discord.com/channels/122739462210846721/122739462210846721/1128677171813158982)', 'https://discord.com/channels/122739462210846721/528742785935998979/1128418716904869980)', 'https://discord.com/channels/122739462210846721/608746838333587456/1128051838831308903)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127643975268974672)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127642692550139974)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127638242842390600)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127619067814105178)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127615159700029553)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127604945550585856)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127340442632081579)', 'https://discord.com/channels/122739462210846721/122739462210846721/1127341937767239781)', 'https://discord.com/channels/122739462210846721/122739462210846721/1126871291786444840)', 'https://discord.com/channels/122739462210846721/122739462210846721/1126863512602431598)', 'https://discord.com/channels/122739462210846721/122739462210846721/1126483095747579934)', 'https://discord.com/channels/122739462210846721/122739462210846721/1126247418854395924)', 'https://discord.com/channels/122739462210846721/122739462210846721/1126236129281191986)', 'https://discord.com/channels/122739462210846721/122739462210846721/1126116156604952646)', 'https://discord.com/channels/122739462210846721/608746838333587456/1125851320503500820)', 'https://discord.com/channels/122739462210846721/122739462210846721/1125521650583093408)', 'https://discord.com/channels/122739462210846721/122739462210846721/1125037231296499825)', 'https://discord.com/channels/122739462210846721/122739462210846721/1124804062622257233)', 'https://discord.com/channels/122739462210846721/486547650976677899/1124654702630535199)', 'https://discord.com/channels/122739462210846721/122739462210846721/1124617815446519933)', 'https://discord.com/channels/122739462210846721/122739462210846721/1124053609420701706)', 'https://discord.com/channels/122739462210846721/122739462210846721/1123655448709574689)', 'https://discord.com/channels/122739462210846721/122739462210846721/1121521322518908928)', 'https://discord.com/channels/122739462210846721/122739462210846721/1121045200287060100)', 'https://discord.com/channels/122739462210846721/122739462210846721/1121030351175827466)', 'https://discord.com/channels/122739462210846721/122739462210846721/1120307084475498497)', 'https://discord.com/channels/122739462210846721/528742785935998979/1119965782051409980)', 'https://discord.com/channels/122739462210846721/122739462210846721/1119562313893159022)', 'https://discord.com/channels/122739462210846721/122739462210846721/1119561700564291644)', 'https://discord.com/channels/122739462210846721/122739462210846721/1119256615699353750)', 'https://discord.com/channels/122739462210846721/122739462210846721/1119208873979551776)', 'https://discord.com/channels/122739462210846721/608785121449082898/1119168072020918352)', 'https://discord.com/channels/122739462210846721/528742785935998979/1118880292992725053)', 'https://discord.com/channels/122739462210846721/486547650976677899/1118455967273713684)', 'https://discord.com/channels/122739462210846721/122739462210846721/1118063318012276796)', 'https://discord.com/channels/122739462210846721/486547650976677899/1117932276211273759)', 'https://discord.com/channels/122739462210846721/860154286141997056/1116734457899143351)', 'https://discord.com/channels/122739462210846721/122739462210846721/1115266255918739487)', 'https://discord.com/channels/122739462210846721/528742785935998979/1114221021088718848)', 'https://discord.com/channels/122739462210846721/122739462210846721/1113952174670610473)', 'https://discord.com/channels/122739462210846721/122739462210846721/1113834497776046120)', 'https://discord.com/channels/122739462210846721/122739462210846721/1112150785028014130)', 'https://discord.com/channels/122739462210846721/528742785935998979/1110191378476060762)', 'https://discord.com/channels/122739462210846721/828045747101499462/1109877140087914577)', 'https://discord.com/channels/122739462210846721/828045747101499462/1109896583455182948)', 'https://discord.com/channels/122739462210846721/608746838333587456/1109893006850523186)', 'https://discord.com/channels/122739462210846721/614191599433547786/1109582587757858846)', 'https://discord.com/channels/122739462210846721/122739462210846721/1109469830127570985)', 'https://discord.com/channels/122739462210846721/122739462210846721/1109231337367417053)', 'https://discord.com/channels/122739462210846721/528742785935998979/1108664436408995890)', 'https://discord.com/channels/122739462210846721/486547650976677899/1108439710877089843)', 'https://discord.com/channels/122739462210846721/528742785935998979/1108314927409672262)', 'https://discord.com/channels/122739462210846721/122739462210846721/1108056962190544948)', 'https://discord.com/channels/122739462210846721/122739462210846721/1108014184433733644)', 'https://discord.com/channels/122739462210846721/122739462210846721/1107722093006696568)', 'https://discord.com/channels/122739462210846721/122739462210846721/1107723992556638329)', 'https://discord.com/channels/122739462210846721/122739462210846721/1107720708219469835)', 'https://discord.com/channels/122739462210846721/122739462210846721/1107604452233457676)', 'https://discord.com/channels/122739462210846721/608785121449082898/1107303660154785813)', 'https://discord.com/channels/122739462210846721/486547650976677899/1106621537651544126)', 'https://discord.com/channels/122739462210846721/528742785935998979/1106316485741252608)', 'https://discord.com/channels/122739462210846721/122739462210846721/1105848390631297115)', 'https://discord.com/channels/122739462210846721/122739462210846721/1105772286344179712)', 'https://discord.com/channels/122739462210846721/528742785935998979/1105787907744215100)', 'https://discord.com/channels/122739462210846721/122739462210846721/1103338191462875176)', 'https://discord.com/channels/122739462210846721/122739462210846721/1103283867600814080)', 'https://discord.com/channels/122739462210846721/122739462210846721/1103244778264592445)', 'https://discord.com/channels/122739462210846721/122739462210846721/1100763713264427049)', 'https://discord.com/channels/122739462210846721/122739462210846721/1100723817099300916)', 'https://discord.com/channels/122739462210846721/122739462210846721/1099092350095065249)', 'https://discord.com/channels/122739462210846721/486547650976677899/1098699884795789514)', 'https://discord.com/channels/122739462210846721/122739462210846721/1097837475449274378)', 'https://discord.com/channels/122739462210846721/122739462210846721/1097821641335132292)', 'https://discord.com/channels/122739462210846721/122739462210846721/1097525141220634805)', 'https://discord.com/channels/122739462210846721/122739462210846721/1097511268690165760)', 'https://discord.com/channels/122739462210846721/122739462210846721/1097431269178085517)', 'https://discord.com/channels/122739462210846721/122739462210846721/1096555088350294136)', 'https://discord.com/channels/122739462210846721/122739462210846721/1095768479711363092)', 'https://discord.com/channels/122739462210846721/635242159880273921/1092923514912256030)', 'https://discord.com/channels/122739462210846721/122739462210846721/1092875035649261730)', 'https://discord.com/channels/122739462210846721/122739462210846721/1092756240729395230)', 'https://discord.com/channels/122739462210846721/122739462210846721/1091819932754378802)', 'https://discord.com/channels/122739462210846721/528742785935998979/1091331444917411911)', 'https://discord.com/channels/122739462210846721/122739462210846721/1090580910950326332)', 'https://discord.com/channels/122739462210846721/122739462210846721/1087849124340183131)', 'https://discord.com/channels/122739462210846721/122739462210846721/1086781827932495993)', 'https://discord.com/channels/122739462210846721/122739462210846721/1086387083742027786)', 'https://discord.com/channels/122739462210846721/122739462210846721/1086018964775260160)', 'https://discord.com/channels/122739462210846721/122739462210846721/1085615580964466778)', 'https://discord.com/channels/122739462210846721/122739462210846721/1085602803038310511)', 'https://discord.com/channels/122739462210846721/122739462210846721/1085576356550684824)', 'https://discord.com/channels/122739462210846721/122739462210846721/1085517825495547965)', 'https://discord.com/channels/122739462210846721/122739462210846721/1085517398314078208)', 'https://discord.com/channels/122739462210846721/769960530290147378/1085511954405273630)', 'https://discord.com/channels/122739462210846721/122739462210846721/1085314176479674470)', 'https://discord.com/channels/122739462210846721/122739462210846721/1084505076929941634)', 'https://discord.com/channels/122739462210846721/769960530290147378/1083808209560674415)', 'https://discord.com/channels/122739462210846721/614191599433547786/1081984878788235464)', 'https://discord.com/channels/122739462210846721/614191599433547786/1081949025785360424)', 'https://discord.com/channels/122739462210846721/528742785935998979/1081157449857388585)', 'https://discord.com/channels/122739462210846721/528742785935998979/1080796528207200308)', 'https://discord.com/channels/122739462210846721/122739462210846721/1080619474178281483)', 'https://discord.com/channels/122739462210846721/122739462210846721/1080615968562237592)', 'https://discord.com/channels/122739462210846721/122739462210846721/1080503067285393480)', 'https://discord.com/channels/122739462210846721/122739462210846721/1080439810579234877)', 'https://discord.com/channels/122739462210846721/122739462210846721/967545764127584338)', 'https://discord.com/channels/122739462210846721/122739462210846721/1078828739456139314)', 'https://discord.com/channels/122739462210846721/769960530290147378/1078816252539179108)', 'https://discord.com/channels/122739462210846721/122739462210846721/1077617598390358106)', 'https://discord.com/channels/122739462210846721/614191599433547786/1077331187787370617)', 'https://discord.com/channels/122739462210846721/122739462210846721/1076091018836971551)', 'https://discord.com/channels/122739462210846721/528742785935998979/1075760678368985098)', 'https://discord.com/channels/122739462210846721/122739462210846721/1075377712065155134)', 'https://discord.com/channels/122739462210846721/122739462210846721/1075040790981644381)', 'https://discord.com/channels/122739462210846721/122739462210846721/1075031868145143879)', 'https://discord.com/channels/122739462210846721/122739462210846721/1075007108208144424)', 'https://discord.com/channels/122739462210846721/122739462210846721/1074723313668071506)', 'https://discord.com/channels/122739462210846721/122739462210846721/1074038704655564850)', 'https://discord.com/channels/122739462210846721/614191599433547786/1074026463487070221)', 'https://discord.com/channels/122739462210846721/122739462210846721/1073969882657468417)', 'https://discord.com/channels/122739462210846721/122739462210846721/1073701873770561596)', 'https://discord.com/channels/122739462210846721/122739462210846721/1073610256376139776)', 'https://discord.com/channels/122739462210846721/122739462210846721/1073604413316415598)', 'https://discord.com/channels/122739462210846721/860154286141997056/1073363406578520124)', 'https://discord.com/channels/122739462210846721/122739462210846721/1073011564153671731)', 'https://discord.com/channels/122739462210846721/860154286141997056/1072991946244620478)', 'https://discord.com/channels/122739462210846721/122739462210846721/1072987352240230554)', 'https://discord.com/channels/122739462210846721/122739462210846721/1072543424269516950)', 'https://discord.com/channels/122739462210846721/122739462210846721/1072129361320349757)', 'https://discord.com/channels/122739462210846721/122739462210846721/1071909384990507028)', 'https://discord.com/channels/122739462210846721/122739462210846721/1071576287078002688)', 'https://discord.com/channels/122739462210846721/860154286141997056/1071432290200211546)', 'https://discord.com/channels/122739462210846721/122739462210846721/1071200327862337657)', 'https://discord.com/channels/122739462210846721/122739462210846721/1070309533496389724)', 'https://discord.com/channels/122739462210846721/122739462210846721/1070034940172963920)', 'https://discord.com/channels/122739462210846721/122739462210846721/1070028784536928256)', 'https://discord.com/channels/122739462210846721/122739462210846721/1069943442047770684)', 'https://discord.com/channels/122739462210846721/122739462210846721/1069930534203031603)', 'https://discord.com/channels/122739462210846721/122739462210846721/1069236574237245451)', 'https://discord.com/channels/122739462210846721/528742785935998979/1069200064163098685)', 'https://discord.com/channels/122739462210846721/528742785935998979/1069050228835111003)', 'https://discord.com/channels/122739462210846721/608785121449082898/1068933668988538890)', 'https://discord.com/channels/122739462210846721/528742785935998979/1068474367639552092)', 'https://discord.com/channels/122739462210846721/769960530290147378/1068407187648548904)', 'https://discord.com/channels/122739462210846721/122739462210846721/1068139319052730449)', 'https://discord.com/channels/122739462210846721/528742785935998979/1068079669678723103)', 'https://discord.com/channels/122739462210846721/528742785935998979/1068080244113821736)', 'https://discord.com/channels/122739462210846721/528742785935998979/1067790357087145984)', 'https://discord.com/channels/122739462210846721/608785121449082898/1067479746214105201)', 'https://discord.com/channels/122739462210846721/122739462210846721/1067410894029590629)', 'https://discord.com/channels/122739462210846721/122739462210846721/1067207975321743442)', 'https://discord.com/channels/122739462210846721/122739462210846721/1066027987054624808)', 'https://discord.com/channels/122739462210846721/528742785935998979/1065970798801719399)', 'https://discord.com/channels/122739462210846721/122739462210846721/1065567540086050887)', 'https://discord.com/channels/122739462210846721/122739462210846721/1065566901721366588)', 'https://discord.com/channels/122739462210846721/122739462210846721/1065339049956622476)', 'https://discord.com/channels/122739462210846721/122739462210846721/1064971680641986640)', 'https://discord.com/channels/122739462210846721/122739462210846721/1064541211437830305)', 'https://discord.com/channels/122739462210846721/614191599433547786/1064338725724758027)', 'https://discord.com/channels/122739462210846721/860154286141997056/1063225351070822544)', 'https://discord.com/channels/122739462210846721/486547650976677899/1062399487282253865)', 'https://discord.com/channels/122739462210846721/122739462210846721/1062131890972266576)', 'https://discord.com/channels/122739462210846721/608785121449082898/1061594677561790484)', 'https://discord.com/channels/122739462210846721/122739462210846721/1061463501572427806)', 'https://discord.com/channels/122739462210846721/122739462210846721/1060990713669632061)', 'https://discord.com/channels/122739462210846721/528742785935998979/1060878730353971240)', 'https://discord.com/channels/122739462210846721/122739462210846721/1059805031932637204)', 'https://discord.com/channels/122739462210846721/122739462210846721/1059463889441525900)', 'https://discord.com/channels/122739462210846721/122739462210846721/1059203109202690209)']
        urls = [s.replace(")", "") for s in urls]

        star_counts = {}
        max_number = len(urls)


        for index, url in enumerate(urls, start=1):
            os.system('clear')
            print(f"{index}/{max_number}")
            # Extract channel_id and message_id from the URL
            match = re.search(r'/channels/\d+/(\d+)/(\d+)', url)
            if match:
                channel_id, message_id = map(int, match.groups())
                channel = self.bot.get_channel(channel_id)

                if channel:
                    try:
                        message = await channel.fetch_message(message_id)
                        # Count the number of yellow star reactions
                        star_reaction = next((reaction for reaction in message.reactions if str(reaction.emoji) == '⭐'), None)
                        if star_reaction:
                            star_counts[url] = star_reaction.count
                        else:
                            star_counts[url] = 0
                    except discord.NotFound:
                        print(f"Message not found for URL: {url}")
                    except discord.Forbidden:
                        print(f"Missing permissions to access message for URL: {url}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

        # Sort the dictionary by the number of stars
        sorted_star_counts = dict(sorted(star_counts.items(), key=lambda item: item[1], reverse=True))

        # Output the sorted results
        for url, count in sorted_star_counts.items():
            print(f"{url} : {count} Sterne")
'''

def setup(bot):
    bot.add_cog(Star(bot, bot.db))


def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)


def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    try:
        channel = make_sequence(channel)
        author = make_sequence(author)
        content = make_sequence(content)
        if lower:
            content = tuple(c.lower() for c in content)

        def check(message):
            if ignore_bot and message.author.bot:
                return False
            if channel and message.channel not in channel:
                return False
            if author and message.author not in author:
                return False
            actual_content = message.content.lower() if lower else message.content
            if content and actual_content not in content:
                return False
            return True

        return check
    except Exception as e:
        logger.error(e)
