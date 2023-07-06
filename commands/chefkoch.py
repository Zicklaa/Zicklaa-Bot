import logging
import random
from get_chefkoch import Recipe, Search

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Chefkoch")


class Chefkoch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ck(self, ctx, *options):
        try:
            if len(options) == 1:
                text = options[0]
            else:
                text = ""
                for option in options:
                    text = text + option + " "
            text = text.lower()
            if len(text) > 100:
                await ctx.reply("Zu viel Junge.")
                logger.info(
                    f"Request from {ctx.author.name}. Chefkoch zu viele Zutaten."
                )
            else:
                if text == "":
                    await ctx.reply("Gib halt wenigstens ne Zutat.")
                    logger.info(
                        f"Request from {ctx.author.name}. Chefkoch keine Zutaten."
                    )
                else:
                    if text == "rotd":
                        recipe = Search().recipeOfTheDay()
                        id = recipe.id
                    else:
                        suche = Search(text)
                        recipe = suche.recipes(limit=5)
                        length = len(recipe)
                        random_number = random.randint(0, length)
                        id = recipe[random_number].id
                    adresse = "https://www.chefkoch.de/rezepte/" + id
                    await ctx.reply(adresse + "\n" + "SCHMEEECKT :DDD")
                    logger.info("Chefkoch für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Request from {ctx.author.name}. Chefkoch.")


def setup(bot):
    bot.add_cog(Chefkoch(bot))
