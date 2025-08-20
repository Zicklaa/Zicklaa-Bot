from email import message
import logging
import random
import discord
import datetime
import asyncio

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Poll")


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def poll(self, ctx, umfragedauer, question, *options: str):
        try:
            try:
                umfragedauer = int(umfragedauer)
                if 0 < umfragedauer < 60:
                    if len(options) > 5:
                        await ctx.reply("Bidde weniger als 5 Optionen kthxbye")
                    elif len(options) < 2:
                        await ctx.reply("Bidde gib mindestens 2 Optionen kthxbye")
                    elif len(question) > 200:
                        await ctx.reply(
                            "Frage bitte nicht länger als ~~mein Cock~~ 200 Chars kthxbye"
                        )
                    else:
                        text = ""
                        i = 1
                        for option in options:
                            if len(option) > 200:
                                await ctx.reply(
                                    "Optionen bitte nicht länger als ~~mein Cock~~ 200 Chars kthxbye"
                                )
                            else:
                                text = text + str(i) + ": " + option + "\n"
                                i = i + 1
                        embed = discord.Embed(
                            title="Poll",
                            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        )
                        embed.set_thumbnail(
                            url="https://cdn-icons-png.flaticon.com/512/3100/3100212.png"
                        )
                        embed.add_field(name=question, value=text, inline=False)
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(
                            text="Umfragedauer: " + str(umfragedauer) + " Minuten"
                        )
                        poll_message = await ctx.reply(embed=embed)
                        for i in range(len(options)):
                            if i == 0:
                                emoji = "1️⃣"
                            elif i == 1:
                                emoji = "2️⃣"
                            elif i == 2:
                                emoji = "3️⃣"
                            elif i == 3:
                                emoji = "4️⃣"
                            elif i == 4:
                                emoji = "5️⃣"
                            await poll_message.add_reaction(emoji)
                        await asyncio.sleep(umfragedauer * 60)
                        cache_msg = discord.utils.get(
                            self.bot.cached_messages, id=poll_message.id
                        )
                        reactions = cache_msg.reactions
                        await poll_message.add_reaction("❌")
                        poll_dict = {}
                        for i in range(len(options)):
                            poll_dict.update({reactions[i].emoji: reactions[i].count})
                        sorted_dict = dict(
                            sorted(
                                poll_dict.items(),
                                key=lambda item: item[1],
                                reverse=True,
                            )
                        )
                        first_pair = list(sorted_dict.items())[0]
                        second_pair = list(sorted_dict.items())[1]
                        if int(first_pair[1]) == int(second_pair[1]):
                            await poll_message.reply(
                                "Es gab keinen eindeutigen Sieger :("
                            )
                        else:
                            if first_pair[0] == "1️⃣":
                                text = "Option 1: **" + options[0] + "** hat gewonnen!"
                            elif first_pair[0] == "2️⃣":
                                text = "Option 2: **" + options[1] + "** hat gewonnen!"
                            elif first_pair[0] == "3️⃣":
                                text = "Option 3: **" + options[2] + "** hat gewonnen!"
                            elif first_pair[0] == "4️⃣":
                                text = "Option 4: **" + options[3] + "** hat gewonnen!"
                            elif first_pair[0] == "5️⃣":
                                text = "Option 5: **" + options[4] + "** hat gewonnen!"
                            await poll_message.reply(question + "\n" + text)
                        logger.info("Poll für: " + ctx.author.name)
                else:
                    await ctx.reply("Dauer bitte zwischen 1 und 60 Minuten.")
                    logger.error("Poll für: " + ctx.author.name)
            except Exception as e:
                await ctx.reply("Als Dauer bitte eine Zahl in Minuten eingeben.")
                logger.error("Poll für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Poll from {ctx.author.name}: {e}")


async def setup(bot):
    await bot.add_cog(Poll(bot))
