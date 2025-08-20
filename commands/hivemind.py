from datetime import datetime
import time
import logging
import discord
import json
import markovify
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Hivemind")


am = discord.AllowedMentions(
    users=False,  # Whether to ping individual user @mentions
    everyone=False,  # Whether to ping @everyone or @here mentions
    roles=False,  # Whether to ping role @mentions
    replied_user=False,  # Whether to ping on replies to messages
)

ratio = 0.7


class Hivemind(commands.Cog):
    def __init__(self, bot, json_model):
        self.bot = bot
        self.json_model = json_model

    @commands.hybrid_command()
    async def hm(self, ctx):
        try:
            while True:
                # satz = json_model.make_short_sentence(140)
                satz = self.json_model.make_sentence(max_overlap_ratio=ratio)
                if satz:
                    await ctx.reply(satz, allowed_mentions=am)
                    break

            logger.info("Hivemind für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")

    @commands.hybrid_command()
    async def hmm(self, ctx):
        if ctx.channel.id == 528742785935998979:
            try:
                for _ in range(5):
                    while True:
                        # satz = json_model.make_short_sentence(140)
                        satz = self.json_model.make_sentence(
                            max_overlap_ratio=ratio,
                        )
                        if satz:
                            await ctx.reply(satz, allowed_mentions=am)
                            break

                logger.info("Hivemind für: " + ctx.author.name)

            except Exception as e:
                await ctx.reply("Klappt nit lol 🤷")
                logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"Hippomode ERROR von {ctx.author.name}")

    '''@commands.hybrid_command()
    async def scrape(self, ctx):
        
        START_DATE = datetime(2024, 1, 4)
        
        try:
            if ctx.author.id == 288413759117066241:
                print("scraping")
                #await ctx.reply("Scrape alle Nachrichten nach dem 20.05.2022 von diesem Channel.")
                #time.sleep(10)
                #await ctx.reply("o man das wird dauern 😂")
                messages = await ctx.channel.history(limit=100000, after=START_DATE).flatten()
                    
                with open("/home/zicklaa/Zicklaa-Bot/static/20-05-2024/hivemind_main_7.txt", "a", encoding="utf-8") as f:
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
                            print('ERROR' + message.content)
                            pass
                print("done")
                #logger.info("Hivemind Scrap für: " + ctx.author.name)
            else:
                await ctx.reply("Nur für Chads, Moruk")

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            # logger.error(f"Hivemind ERROR von {ctx.author.name}: {e}")
            '''
    
    '''@commands.hybrid_command()
    async def compile(self, ctx):
        with open('/home/zicklaa/Zicklaa-Bot/static/20-05-2024/merged_file.txt', 'r', encoding="utf-8") as f:
            print("Chaining the Chain")
            text = f.read()
        text_model = markovify.NewlineText(text, state_size=2, well_formed=False)
        text_model = text_model.compile()
        model_json = text_model.to_json()
        with open('hivemind_20-05-2024-wff.json', 'w', encoding='utf-8') as f:
            json.dump(model_json, f)
        print("compiled")'''


async def setup(bot):
    await bot.add_cog(Hivemind(bot, bot.json_model))
