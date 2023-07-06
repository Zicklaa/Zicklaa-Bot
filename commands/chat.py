import logging

import openai
from discord.ext import commands
import discord
from datetime import datetime


logger = logging.getLogger("ZicklaaBot.Chat")


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chat(self, ctx, *text):
        openai.api_key = self.bot.OPENAI_API_KEY
        async with ctx.channel.typing():
            try:
                text = " ".join(text)
                text = text.replace('"', "")
                if text:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        max_tokens=500,
                        messages=[{"role": "user", "content": text}],
                    )
                    antwort = completion["choices"][0]["message"]["content"]
                    kosten = completion["usage"]["total_tokens"]
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    if len(antwort) > 1023:
                        if len(antwort) > 2000:
                            await ctx.reply("Antwort leider zu lang für Discord :(")
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
                                + str((kosten * 0.0002))
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
                            + str((kosten * 0.0002))
                            + " Cent"
                        )
                        await ctx.reply(embed=embed)

                        logger.info("Chat gepostet für " + ctx.author.name)
                else:
                    await ctx.reply("Brauch schon nen Text von dir du Lellek.")
                    logger.info("Chat kein Text von " + ctx.author.name)
            except Exception as e:
                await ctx.reply("Fühl mich heute nicht nach Konversation :(")
                logger.error(f"Chat Error from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Chat(bot))
