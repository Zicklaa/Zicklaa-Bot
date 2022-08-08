import logging
import discord
import json
import markovify
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Hivemind")


'''with open('/home/zicklaa/Zicklaa-Bot/static/25-07-2022/hivemind_merged.txt', 'r', encoding="utf-8") as f:
    print("Chaining the Chain")
    text = f.read()
text_model = markovify.NewlineText(text, state_size=2, well_formed=True)
text_model = text_model.compile()
model_json = text_model.to_json()
with open('hivemind_ss2.json', 'w', encoding='utf-8') as f:
    json.dump(model_json, f)
print("compiled")'''


am = discord.AllowedMentions(
    users=False,         # Whether to ping individual user @mentions
    everyone=False,      # Whether to ping @everyone or @here mentions
    roles=False,         # Whether to ping role @mentions
    replied_user=False,  # Whether to ping on replies to messages
)

ratio = 0.65


class Hivemind(commands.Cog):
    def __init__(self, bot, json_model):
        self.bot = bot
        self.json_model = json_model

    @commands.command()
    async def hm(self, ctx):
        try:
            while True:
                # satz = json_model.make_short_sentence(140)
                satz = self.json_model.make_sentence(
                    max_overlap_ratio=ratio)
                if satz:
                    await ctx.reply(satz, allowed_mentions=am)
                    break

            logger.info("Hivemind für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")

    @commands.command()
    async def hmm(self, ctx):
        if ctx.channel.id == 528742785935998979:
            try:
                for _ in range(5):
                    while True:
                        # satz = json_model.make_short_sentence(140)
                        satz = self.json_model.make_sentence(
                            max_overlap_ratio=ratio,)
                        if satz:
                            await ctx.reply(satz, allowed_mentions=am)
                            break

                logger.info("Hivemind für: " + ctx.author.name)

            except Exception as e:
                await ctx.reply("Klappt nit lol 🤷")
                logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.error(f"Hippomode ERROR von {ctx.author.name}")

    '''@commands.command()
    async def scrape(self, ctx):
        try:
            if ctx.author.id == 288413759117066241:
                print("scraping")
                await ctx.reply("Scrape 10.000 Nachrichten von diesem Channel")
                messages = await ctx.channel.history(limit=10000).flatten()
                with open("/home/zicklaa/Zicklaa-Bot/static/25-07-2022/hivemind_durstaufwurst.txt", "a", encoding="utf-8") as f:
                    for message in messages:
                        try:
                            if message.content == '' or message.content.startswith('<') or message.content.startswith('https') \
                                    or message.content.startswith('+') or message.content.startswith('$') or message.author.bot \
                                    or message.content.startswith('http') or message.content.startswith('.') or message.content.startswith('!')\
                                    or message.content.startswith('?'):
                                print('passed')
                            else:
                                f.write(message.content + "\n")
                                print(message.content)
                        except:
                            print('ERROR')
                            pass
                print("done")
                #logger.info("Hivemind Scrap für: " + ctx.author.name)
            else:
                await ctx.reply("Nur für Chads, Moruk")

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            # logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")'''


def setup(bot):
    bot.add_cog(Hivemind(bot, bot.json_model))
