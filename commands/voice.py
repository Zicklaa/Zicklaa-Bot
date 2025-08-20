import logging
from discord.ext import commands
import discord
from gtts import gTTS
from random import randint

logger = logging.getLogger("ZicklaaBot.Voice")
voice_channel = 608785371135737878
language = "de"
ratio = 0.65

am = discord.AllowedMentions(
    users=False,  # Whether to ping individual user @mentions
    everyone=False,  # Whether to ping @everyone or @here mentions
    roles=False,  # Whether to ping role @mentions
    replied_user=False,  # Whether to ping on replies to messages
)


class Voice(commands.Cog):
    def __init__(self, bot, json_model):
        self.bot = bot
        self.json_model = json_model

    @commands.hybrid_command()
    async def ttshm(self, ctx):
        try:
            global vc

            while True:
                satz = self.json_model.make_sentence(max_overlap_ratio=ratio)
                if satz:
                    break
            tts = gTTS(text=satz, lang=language, slow=False)
            file_path = "static/sounds/ttshm.mp3"
            tts.save(file_path)
            vc.play((discord.FFmpegPCMAudio(file_path)))
            await ctx.reply(satz, allowed_mentions=am)
        except:
            await ctx.message.delete()
            logger.error(f"Voicechat Play from {ctx.author.name}")

    @commands.hybrid_command()
    async def tts(self, ctx, *text):
        try:
            global vc
            satz = " ".join(text)
            tts = gTTS(text=satz, lang=language, slow=False)
            file_path = "static/sounds/tts.mp3"
            tts.save(file_path)
            vc.play((discord.FFmpegPCMAudio(file_path)))
        except:
            await ctx.message.delete()
            logger.error(f"Voicechat Play from {ctx.author.name}")

    @commands.hybrid_command()
    async def join(self, ctx):
        try:
            channel = self.bot.get_channel(voice_channel)
            global vc
            vc = await channel.connect()
            await ctx.message.delete()
        except:
            await ctx.message.delete()
            logger.error(f"Voicechat Join from {ctx.author.name}")

    @commands.hybrid_command()
    async def leave(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            await server.disconnect()
            await ctx.message.delete()
        except:
            await ctx.message.delete()
            logger.error(f"Voicechat Leave from {ctx.author.name}")


async def setup(bot):
    await bot.add_cog(Voice(bot, bot.json_model))
