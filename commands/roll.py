import logging
import random
import discord

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Roll")


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def roll(self, ctx, *nummern):
        try:
            if nummern:
                if len(nummern) > 2:
                    await ctx.reply("Zu viele Argumente, Kollege.")
                    logger.info("roll(): Zu viele Argumente: " + ctx.author.name)
                elif len(nummern) == 1:
                    zahl = int(nummern[0])
                    if isinstance(zahl, int):
                        if zahl > 0:
                            await ctx.reply(random.randint(1, zahl))
                            logger.info("Dice Roll für: " + ctx.message.author.name)
                        else:
                            await ctx.reply("Zahl ist zu klein, du Monger.")
                            logger.info("roll(): Zahl zu klein von: " + ctx.author.name)
                    else:
                        await ctx.reply("Das is keine Zahl, du Monger.")
                        logger.info("roll(): Keine Zahl von: " + ctx.author.name)
                else:
                    zahl1 = int(nummern[0])
                    zahl2 = int(nummern[1])
                    if isinstance(zahl1, int) and isinstance(zahl2, int):
                        if zahl1 > 0 and zahl2 > 0:
                            if zahl1 > 20:
                                await ctx.reply(
                                    "Pls nicht mehr als 10 Würfe auf einmal."
                                )
                                logger.info(
                                    "roll(): Zu viele Würfe: " + ctx.author.name
                                )
                            else:
                                würfe = ""
                                i = 1
                                add = 0
                                for x in range(zahl1):
                                    wurf = random.randint(1, zahl2)
                                    add = add + wurf
                                    würfe = (
                                        würfe
                                        + "Wurf "
                                        + str(i)
                                        + ": "
                                        + str(wurf)
                                        + "\n"
                                    )
                                    i = i + 1
                                würfe = würfe + "Gesamt: " + str(add)
                                embed = discord.Embed(
                                    title="Würfelwurf",
                                    description="Veni Vidi Ficki",
                                    color=0x00FF00,
                                )
                                embed.set_author(
                                    name="Gott",
                                    icon_url="https://upload.wikimedia.org/wikipedia/commons/7/7c/Cima_da_Conegliano%2C_God_the_Father.jpg",
                                )
                                embed.add_field(
                                    name=str(zahl1) + "d" + str(zahl2),
                                    value=würfe,
                                    inline=False,
                                )
                                await ctx.reply(embed=embed)
                                logger.info("Dice Roll für: " + ctx.message.author.name)
                        else:
                            await ctx.reply("Zahl ist zu klein, du Monger.")
                            logger.info("roll(): Zahl zu klein von: " + ctx.author.name)
                    else:
                        await ctx.reply("Das is keine Zahl, du Monger.")
                        logger.info("roll(): Keine Zahl von: " + ctx.author.name)
            else:
                await ctx.reply(
                    "Wie soll ich dir etwas rollen wenn du nichtmal Zahlen gibst stellst, du Monger?"
                )
                logger.info("roll(): Keine Frage gestellt von: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Roll from {ctx.author.name}: {e}")


async def setup(bot):
    await bot.add_cog(Roll(bot))
