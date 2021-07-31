import logging
import random

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Magic8")
magic8_list = ["Zu 100% Ja!", "Es ist so entschieden, Ja.","Ja :3 OwO", "Ohne Zweifel, Ja.", "Definitiv, Ja.", "Kannst dich drauf verlassen, Digga.", "So wie ich des seh, scho, Ja.", "Denk scho, Ja.", "Ja.", "Ich hab Dieter um rat gefragt, er sagt Ja.",
                 "Merkur ist rückläufig, also Ja.", "Digga, bin hier grad Ballsdeep in etwas, frag später.", "Du würdest die Wahrheit nicht verkraften.", "Weiß nich, lol.", "Ich schwöre ich hab keine Ahnung von was du redest.", "Musst du Dieter fragen.", "Jesse, von was zum Fick redest du??",
                 "Nein.", "Nein, lol.", "Get fucked Digga, als ob ich dazu Ja sag.", "Du literarischer Untermensch, was stellst du mir so eine kernbehinderte Frage???", "Sieht nicht so aus.", "Würd ich ned drauf wetten.", "Niemals, Kollege.",
                 "Dieter hat Nein gesagt :///", "Ich weiß nicht, aber wie wärs mit Megges?", "Nein, du HUNDT."]

class Magic8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def magic8(self, ctx, *frage):
        async with ctx.channel.typing():
            try:
                if frage:
                    choice = random.choice(magic8_list)
                    await ctx.reply(choice)
                    logger.info("magic8(): Choice gepostet für: " + ctx.author.name)
                else:
                    await ctx.reply("Wie soll ich dir etwas beantworten wenn du nichtmal ne Frage stellst, du Monger?")
                    logger.info("magic8(): Keine Frage gestellt von: " + ctx.author.name)

            except Exception as e:
                await ctx.reply("Klappt nit lol 🤷")
                logger.error(f'Request from {ctx.author.name}: {e}')


def setup(bot):
    bot.add_cog(Magic8(bot))
