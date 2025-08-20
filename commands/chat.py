from io import BytesIO
import logging

import openai
from openai import OpenAI
from discord.ext import commands
import discord
from datetime import datetime
import os
import os

import requests
import fal_client
import fal_client

logger = logging.getLogger("ZicklaaBot.Chat")


class Chat(commands.Cog):
    def __init__(self, bot, json_model):
        self.bot = bot
        self.json_model = json_model
        os.environ["FAL_KEY"] = self.bot.FAL_API_KEY
        os.environ["FAL_KEY"] = self.bot.FAL_API_KEY

    @commands.hybrid_command()
    async def chat(self, ctx, *, text):
        client_OAI = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                try:
                    if text:
                        completion = client_OAI.chat.completions.create(
                            model="gpt-4.1",
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
                                logger.info(
                                    "Chat zu lang für " + ctx.author.name)
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
                                    + str(round(kosten * 0.00000015, 8))
                                    + " Cent"
                                )
                                await ctx.reply(embed=embed)
                                logger.info(
                                    "Chat gepostet für " + ctx.author.name)
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
                            embed.add_field(
                                name="Antwort", value=antwort, inline=False)
                            embed.set_footer(
                                text=str(current_time)
                                + " Uhr | Kosten: "
                                + str(kosten)
                                + " Tokens = "
                                + str(round(kosten * 0.00000015, 8))
                                + " Cent"
                            )
                            await ctx.reply(embed=embed)
                            logger.info(
                                "Chat gepostet für " + ctx.author.name)
                    else:
                        await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                        logger.info("Chat kein Text von " +
                                    ctx.author.name)
                except Exception as e:
                    await ctx.reply(e.message)
                    logger.error(f"Chat Error from {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"Chat außerhalb Meme Channel von {ctx.author.name}")

    @commands.hybrid_command()
    async def hmchat(self, ctx, *, text):
        client_OAI = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                max_attempts = 2
                max_attempts = 2
                attempts = 0
                while True:
                    # satz = json_model.make_short_sentence(140)
                    text = self.json_model.make_sentence(
                        max_overlap_ratio=0.65,
                    )
                    if text:
                        while attempts < max_attempts:
                            try:
                                preprompt = "Du bist Discordnutzer des Discord-Servers >Bens Haus der Enten<. Versuche unter allen umständen auf den folgenden Text zu antworten, auch wenn du ihn vielleicht nicht verstehst. Benutze wenn möglich anglizismen und generelle GEN Z Slang Wörter. Erwähne nicht dass du ein LLM bist oder dass du den Text nicht verstehst. Antworte wie ein cooler Jugendlicher und benutze wenn es passt auch Emojis. Gehe dabei auf alle Elemente des Texts ein. Baue so viel wissen und referenzen ein wie du nur kannst. Der Satz auf den du antworten sollst kommt jetzt:"

                                completion = client_OAI.chat.completions.create(
                                    model="gpt-4o-mini",
                                    max_tokens=500,
                                    messages=[
                                        {"role": "user", "content": preprompt + text}],
                                )
                                antwort = completion.choices[0].message.content
                                kosten = completion.usage.total_tokens
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                if len(antwort) > 1023:
                                    if len(antwort) > 2000:
                                        await ctx.reply("Antwort leider zu lang für Discord :(")
                                        logger.info(
                                            "Chat zu lang für " + ctx.author.name)
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
                                            + str(round(kosten * 0.00000015, 8))
                                            + " Cent"
                                        )
                                        await ctx.reply(text)
                                        await ctx.reply(embed=embed)
                                        logger.info(
                                            "Chat gepostet für " + ctx.author.name)
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
                                    embed.add_field(
                                        name="Antwort", value=antwort, inline=False)
                                    embed.set_footer(
                                        text=str(current_time)
                                        + " Uhr | Kosten: "
                                        + str(kosten)
                                        + " Tokens = "
                                        + str(round(kosten * 0.00000015, 8))
                                        + " Cent"
                                    )
                                    await ctx.reply(text)
                                    await ctx.reply(embed=embed)
                                    logger.info(
                                        "Chat gepostet für " + ctx.author.name)
                                attempts = 999999
                            except Exception as e:
                                await ctx.reply("Irgendwas klappt nit lel.")
                                logger.error(
                                    f"Chat Error from {ctx.author.name}: {e}")
                                attempts += 1
                    break
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"Chat außerhalb Meme Channel von {ctx.author.name}")

    @commands.hybrid_command()
    async def bild(self, ctx, *, text):
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                try:
                    if text:
                        await self.getImage(ctx, text, "image.jpg", "true", "schnell")
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

    @commands.hybrid_command()
    async def nsfw(self, ctx, *, text):
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                try:
                    if text:
                        await self.getImage(ctx, text, "SPOILER_image.jpg", "false", "schnell")
                        logger.info("Porn gepostet für " + ctx.author.name)
                    else:
                        await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                        logger.info("Porn kein Text von " + ctx.author.name)
                except Exception as e:
                    await ctx.reply("Fehler lul")
                    logger.error(f"Porn Error from {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"Porn außerhalb Meme Channel von {ctx.author.name}")

    @commands.hybrid_command()
    async def hd(self, ctx, *, text):
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                try:
                    if text:
                        await self.getImage(ctx, text, "image.jpg", "true", "dev")
                        logger.info("HD gepostet für " + ctx.author.name)
                    else:
                        await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                        logger.info("HD kein Text von " + ctx.author.name)
                except Exception as e:
                    await ctx.reply("Fehler lul")
                    logger.error(f"HD Error from {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"HD außerhalb Meme Channel von {ctx.author.name}")

    @commands.hybrid_command()
    async def hdnsfw(self, ctx, *, text):
        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                try:
                    if text:
                        await self.getImage(ctx, text, "SPOILER_image.jpg", "false", "dev")
                        logger.info("HDNSFW gepostet für " + ctx.author.name)
                    else:
                        await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                        logger.info("HDNSFW kein Text von " + ctx.author.name)
                except Exception as e:
                    await ctx.reply("Fehler lul")
                    logger.error(f"HDNSFW Error from {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"HDNSFW außerhalb Meme Channel von {ctx.author.name}")

    @commands.hybrid_command()
    async def pipeline(self, ctx, *, text):
        client_OAI = OpenAI(api_key=self.bot.OPENAI_API_KEY)

        preprompt = "You will be given user input. Given the user's input message, create a detailed, vivid description to generate a high-quality image using AI. Include specific details about the scene, background, objects, and emotions. Consider the lighting, colors, textures, and any relevant environment or mood. Ensure that the description is coherent and descriptive enough to guide the AI in generating an accurate and visually appealing image. But also keep yourself short and precise as not to overload the image generator with too much input. The output should be a single, comprehensive prompt that fully captures the essence of the user's input. Return only the output. The output has to be in english. Input: "

        if ctx.channel.id == 528742785935998979 or ctx.channel.id == 567411189336768532:
            async with ctx.channel.typing():
                try:
                    if text:
                        completion = client_OAI.chat.completions.create(
                            model="gpt-4.1",
                            max_tokens=500,
                            messages=[
                                {"role": "user", "content": preprompt + text}],
                        )
                        antwort = completion.choices[0].message.content

                        if antwort:
                            await self.getImage(ctx, antwort, "SPOILER_image.jpg", "false", "pipeline")
                            logger.info(
                                "HDNSFW Pipeline gepostet für " + ctx.author.name)
                        else:
                            await ctx.reply("Irgendwas klappt nicht, kb herauszufinden wieso.")
                            logger.info(
                                "HDNSFW Pipeline kein Text von " + ctx.author.name)
                    else:
                        await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                        logger.info(
                            "HDNSFW Pipeline kein Text von " + ctx.author.name)
                except Exception as e:
                    await ctx.reply("Fehler lul")
                    logger.error(f"HDNSFW Error from {ctx.author.name}: {e}")
        else:
            await ctx.reply("Spam woanders, Moruk 🤷")
            logger.info(f"HDNSFW außerhalb Meme Channel von {ctx.author.name}")

    async def getImage(self, ctx, text, imageName, blockNsfw, model):
        if (model == "schnell"):
            num_inference_steps = 2
        elif (model == "pipeline"):
            model = "schnell"
            num_inference_steps = 4
        else:
            num_inference_steps = 28

        handler = fal_client.submit(
            "fal-ai/flux/" + model,
            arguments={
                "prompt": text,
                "num_inference_steps": num_inference_steps,
                "enable_safety_checker": blockNsfw
            },
        )

        antwort = handler.get()
        response = requests.get(url=antwort['images'][0]['url'])
        response.raise_for_status()
        await ctx.reply(file=discord.File(BytesIO(response.content), imageName))

    @commands.hybrid_command()
    async def tts(self, ctx, *, text):
        client_OAI = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        names = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

        first_word = get_first_word(text)

        async with ctx.channel.typing():
            try:
                if (first_word in names):
                    voice = first_word
                    text = text.replace(first_word, "")
                else:
                    voice = "onyx"
                if text:
                    completion = client_OAI.audio.speech.create(
                        model="tts-1-hd",
                        voice=voice,
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


def get_first_word(string):
    words = string.split()
    if words:
        return words[0]
    else:
        return None  # Return None if the string is empty


async def setup(bot):
    await bot.add_cog(Chat(bot, bot.json_model))
