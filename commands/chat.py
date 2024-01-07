from io import BytesIO
import logging

import openai
from openai import OpenAI
from discord.ext import commands
import discord
from datetime import datetime

import requests


logger = logging.getLogger("ZicklaaBot.Chat")


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chat(self, ctx, *text):
        client_OAI = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                max_attempts=2
                attempts = 0
                while attempts < max_attempts:
                    try:
                        text = " ".join(text)
                        text = text.replace('"', "")
                        if text:
                            completion = client_OAI.chat.completions.create(
                                model="gpt-4-1106-preview",
                                max_tokens=500,
                                messages=[{"role": "user", "content": text}],
                            )
                            antwort = completion.choices[0].message.content
                            kosten = completion.usage.total_tokens
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")
                            if len(antwort) > 1023:
                                if len(antwort) > 2000:
                                    await ctx.reply("Antwort leider zu lang für Discord :(")
                                    await ctx.reply(antwort)
                                    logger.info("Chat zu lang für " + ctx.author.name)
                                else:
                                    embed = discord.Embed(
                                        title="Antwort von ChatGPT auf den Prompt",
                                        description=antwort,
                                        color=0x00FF00,
                                    )
                                    embed.set_author(
                                        name="ChatGPT",
                                        icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1024px-ChatGPT_logo.svg.png",
                                    )
                                    embed.set_footer(
                                        text=str(current_time)
                                        + " Uhr | Kosten: "
                                        + str(kosten)
                                        + " Tokens = "
                                        + str(round(kosten * 0.00004, 4))
                                        + " Cent"
                                    )
                                    await ctx.reply(embed=embed)
                                    logger.info("Chat gepostet für " + ctx.author.name)
                            else:
                                embed = discord.Embed(
                                    title="Antwort von ChatGPT auf den Prompt",
                                    description="Prompt: " + text,
                                    color=0x00FF00,
                                )
                                embed.set_author(
                                    name="ChatGPT",
                                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1024px-ChatGPT_logo.svg.png",
                                )
                                embed.add_field(name="Antwort", value=antwort, inline=False)
                                embed.set_footer(
                                    text=str(current_time)
                                    + " Uhr | Kosten: "
                                    + str(kosten)
                                    + " Tokens = "
                                    + str(round(kosten * 0.00004, 4))
                                    + " Cent"
                                )
                                await ctx.reply(embed=embed)
                                logger.info("Chat gepostet für " + ctx.author.name)
                            attempts = 999999
                        else:
                            await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                            logger.info("Chat kein Text von " + ctx.author.name)
                    except Exception as e:
                        logger.error(f"Chat Error from {ctx.author.name}: {e}")
                        attempts += 1
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"Chat außerhalb Meme Channel von {ctx.author.name}")

    @commands.command()
    async def bild(self, ctx, *text):
        client_OAI = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                try:
                    text = " ".join(text)
                    text = text.replace('"', "")
                    if text:
                        completion = client_OAI.images.generate(
                            model="dall-e-3",
                            n=1,
                            size="1024x1024",
                            prompt=text,
                            quality="standard"
                        )
                        antwort = completion.data[0].url

                        response = requests.get(antwort)
                        response.raise_for_status()
                        await ctx.reply(file=discord.File(BytesIO(response.content), 'image.jpg'))
                        logger.info("Bild gepostet für " + ctx.author.name)
                    else:
                        await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                        logger.info("Bild kein Text von " + ctx.author.name)
                except Exception as e:
                    await ctx.reply("Fehler lul")
                    logger.error(f"Bild Error from {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"Bild außerhalb Meme Channel von {ctx.author.name}")

    @commands.command()
    async def tts(self, ctx, *text):
        client_OAI = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        async with ctx.channel.typing():
            try:
                text = " ".join(text)
                text = text.replace('"', "")
                if text:
                    completion = client_OAI.audio.speech.create(
                        model="tts-1-hd",
                        voice="onyx",
                        input=text
                        )
                    mp3_file = BytesIO(completion.content)
                    mp3_file.seek(0)
                    await ctx.reply(file=discord.File(BytesIO(mp3_file.getvalue()), 'tts.mp3'))
                    logger.info("TTS gepostet für " + ctx.author.name)
                else:
                    await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                    logger.info("TTS kein Text von " + ctx.author.name)
            except Exception as e:
                await ctx.reply("Fehler lul")
                logger.error(f"TTS Error from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Chat(bot))
