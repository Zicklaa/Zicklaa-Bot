import logging
import discord
from datetime import datetime
from discord.ext import commands
import random
import time

logger = logging.getLogger("ZicklaaBot.Discordle")

user_list = {
    255843901452189696: "Maik#4496",
    369579608615682071: "Windowmarker#8038",
    122721968406528001: "Lou E Coyote#3879",
    136103007065473024: "Krato#2209",
    240554673134764032: "vergyl#8505",
    288413759117066241: "z++#6969",
    189024459766759424: "exalibur#2817",
    119845703844495360: "Yoshii#0125",
    217030695799881729: "vladoks#9898",
    426347844748705792: "Armlehne#3129",
    227493008130572288: "somehowyellow#3394",
    197036529644863489: "Dinooooo#7276",
    226379429251776512: "grumbel#5982",
    218777864282177546: "Sunshower#2126",
    134035884507922433: "TheDavi#9963",
    191119825353965568: "Anna#0001",
    97427959731720192: "Guy.#2505",
    144981368294604811: "Kahimey#1948",
    370904224034455564: "Teutobald#7131",
    162863123617939456: "Turantel#1596",
    301096437511487498: "This is fine.#0549",
    128263704314773504: "Hebelios#4392",
    305615676544909323: "WMS#0001",
    428974837805875201: "BenSwolo#0751",
    176612606444830720: "Laufamholzer#7435",
    203169780180451328: "Dr Blazing Green Blaze#4072",
    253552795733458944: "Brotmann#5898",
    342019184689152024: "NooGravity#4345",
    205720251789213696: "JonSnowWhite#6467",
    413068385962819584: "galaali#1923",
    156136437887008771: "Dalton#5000",
    169427086539227136: "kyz3#9730",
    165549213378150400: "loixL#1107",
    373135654521143317: "SirTeaRex#2299",
    200009451292459011: "Fritzvonkola#6253",
    177808504881414144: "lucra400#4435",
    184773457005903873: "Zerus#8478",
    274204764068118529: "SpaceHippo#1896",
    232111930351943680: "Wabooti#8101",
    133886693379014656: "Jarmanien#0001",
    165575458954543104: "DieterTheHorst#1357",
    208949142729261056: "Olley#7784",
    148790752254754817: "mbn#0404",
    122738631646511106: "Ben#8168",
    107787146366066688: "Rilko#4768",
    179680865805271040: "&HansTrashy#0001",
    145444659240370176: "locke#5790",
    247064633599459328: "hanfi#8643",
    211519719075741698: "F2#2999",
    157917509046108161: "Flips#0815",
    749235359925272686: "senfglas#6741",
    231527378243813386: "Luca Bazooka#8144",
    148471614483202048: "DonMartino#1000",
    184372370486591489: "Jack#2126",
    192318108990570497: "Khas#2052",
    95480104779526144: "Neriik#1984",
}

unerwuenscht = {
    571051961256902671: "Der Gelbfus Cowboy#1008",
    368105370532577280: "Zapier#0625",
    595627591118094347: 'Axel "Omega Prime" Werner#4331',
    335930325462941698: "Weltherrschaftsbot#7241",
    356268235697553409: ".fmbot#8173",
}

channel_ids = {
    122739462210846721: 1449075600,
    486547650976677899: 1536072480,
    608746970340786282: 1565208000,
    608746838333587456: 1565208000,
    608785121449082898: 1565215200,
    735911531350458368: 1595525400,
    828045747101499462: 1617490800,
    614191599433547786: 1566504000,
    635242159880273921: 1571522400,
    528742785935998979: 1546131600,
    769960530290147378: 1603645200,
    675448334089060409: 1581109200,
    860154286141997056: 1625148000,
}

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
    "mp3",
]


class Discordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def dc(self, ctx):
        try:
            kanal_id, kanal_zeit = random.choice(list(channel_ids.items()))
            kanal = self.bot.get_channel(int(kanal_id))
            random_datum = random_date(int(kanal_zeit))
            messages = await kanal.history(limit=100, around=random_datum).flatten()
            for x in range(200):
                random_message = random.choice(messages)
                result = len(random_message.content.split())
                if (
                    result > 5
                    and result < 50
                    and random_message.author.id not in unerwuenscht
                    and random_message.author.id in user_list
                ):
                    random_users = []
                    random_users.append(str(random_message.author))
                    for x in range(100):
                        temp_rand_user = random.choice(list(user_list.values()))
                        if temp_rand_user not in random_users:
                            random_users.append(temp_rand_user)
                            if len(random_users) == 4:
                                break
                    random.shuffle(random_users)
                    embed = discord.Embed(
                        title="Discordle",
                        description="Welcher User hat dieses lyrische Meisterwerk verfasst?",
                        color=0x00FF00,
                    )
                    embed.set_author(
                        name="Mysteriös",
                        icon_url="https://i.pinimg.com/564x/b5/46/3c/b5463c3591ec63cf076ac48179e3b0db.jpg",
                        url="https://i.pinimg.com/originals/53/c9/a9/53c9a957244f81f276b9845410cfeb5b.jpg",
                    )
                    embed.set_footer(text="Discordle by: " + ctx.author.name)
                    embed.add_field(
                        name="**Runde 1**",
                        value=str(random_message.content),
                        inline=False,
                    )
                    embed.add_field(
                        name="**Runde 2**",
                        value="||"
                        + str(random_message.created_at.strftime("%d.%m.%Y, %H:%M"))
                        + "||",
                        inline=False,
                    )
                    embed.add_field(
                        name="**Runde 3**",
                        value="||#"
                        + str(random_message.channel).ljust(
                            random.randint(25, 50), "\u2000"
                        )
                        + "||",
                        inline=False,
                    )
                    embed.add_field(
                        name="**Runde 4**",
                        value="||"
                        + random_users[0]
                        + "\n"
                        + random_users[1]
                        + "\n"
                        + random_users[2]
                        + "\n"
                        + random_users[3]
                        + "||",
                        inline=False,
                    )
                    embed.add_field(
                        name="**Auflösung**",
                        value="||"
                        + str(random_message.author).ljust(
                            random.randint(25, 50), "\u2000"
                        )
                        + "\n"
                        + "[Link zur Nachricht]("
                        + random_message.jump_url
                        + ")"
                        + "||",
                        inline=False,
                    )
                    break
            try:
                new_message = await ctx.channel.send(embed=embed)
                await ctx.message.delete()
                await new_message.add_reaction("1️⃣")
                await new_message.add_reaction("2️⃣")
                await new_message.add_reaction("3️⃣")
                await new_message.add_reaction("4️⃣")
                await new_message.add_reaction("❌")
            except Exception as e:
                await ctx.reply("Was ist denn mit Karsten los??")
                logger.error("Discordle für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Was ist denn mit Karsten los??")
            logger.error("Discordle für: " + ctx.author.name)

    @commands.hybrid_command()
    async def bc(self, ctx):
        try:
            kanal_id, kanal_zeit = random.choice(list(channel_ids.items()))
            kanal = self.bot.get_channel(int(kanal_id))
            random_datum = random_date(int(kanal_zeit))
            messages = await kanal.history(limit=100, around=random_datum).flatten()
            for x in range(200):
                random_message = random.choice(messages)
                if (
                    random_message.attachments
                    and random_message.author.id not in unerwuenscht
                    and random_message.author.id in user_list
                ):
                    if not any(
                        ext in random_message.attachments[0].url for ext in ext_list
                    ):
                        random_users = []
                        random_users.append(str(random_message.author))
                        for x in range(100):
                            temp_rand_user = random.choice(list(user_list.values()))
                            if temp_rand_user not in random_users:
                                random_users.append(temp_rand_user)
                                if len(random_users) == 4:
                                    break
                        random.shuffle(random_users)
                        embed = discord.Embed(
                            title="Bildcordle",
                            description="Welcher User hat dieses optische Meisterwerk verfasst?",
                            color=0x00FF00,
                        )
                        embed.set_author(
                            name="Mysteriös",
                            icon_url="https://i.pinimg.com/564x/b5/46/3c/b5463c3591ec63cf076ac48179e3b0db.jpg",
                            url="https://i.pinimg.com/originals/53/c9/a9/53c9a957244f81f276b9845410cfeb5b.jpg",
                        )
                        embed.set_footer(text="Discordle by: " + ctx.author.name)
                        embed.set_image(url=str(random_message.attachments[0].url))
                        embed.add_field(
                            name="**Runde 1**", value="Siehe Bild", inline=False
                        )
                        embed.add_field(
                            name="**Runde 2**",
                            value="||"
                            + str(random_message.created_at.strftime("%d.%m.%Y, %H:%M"))
                            + "||",
                            inline=False,
                        )
                        embed.add_field(
                            name="**Runde 3**",
                            value="||#"
                            + str(random_message.channel).ljust(
                                random.randint(25, 50), "\u2000"
                            )
                            + "||",
                            inline=False,
                        )
                        embed.add_field(
                            name="**Runde 4**",
                            value="||"
                            + random_users[0]
                            + "\n"
                            + random_users[1]
                            + "\n"
                            + random_users[2]
                            + "\n"
                            + random_users[3]
                            + "||",
                            inline=False,
                        )
                        embed.add_field(
                            name="**Auflösung**",
                            value="||"
                            + str(random_message.author).ljust(
                                random.randint(25, 50), "\u2000"
                            )
                            + "\n"
                            + "[Link zur Nachricht]("
                            + random_message.jump_url
                            + ")"
                            + "||",
                            inline=False,
                        )
                        break
            try:
                new_message = await ctx.channel.send(embed=embed)
                await ctx.message.delete()
                await new_message.add_reaction("1️⃣")
                await new_message.add_reaction("2️⃣")
                await new_message.add_reaction("3️⃣")
                await new_message.add_reaction("4️⃣")
                await new_message.add_reaction("❌")
            except Exception as e:
                await ctx.reply("Was ist denn mit Karsten los??")
                logger.error("Bildcordle für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Was ist denn mit Karsten los??")
            logger.error("Bildcordle für: " + ctx.author.name)


def random_date(kanal_zeit):
    start = kanal_zeit
    current = int(time.time())
    random_unixstamp = random.randint(start, current)
    return datetime.fromtimestamp(random_unixstamp)


async def setup(bot):
    await bot.add_cog(Discordle(bot))
