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
            if len(options) > 1:
                await ctx.reply("Bitte erstmal nur eine Zutat.")
                logger.info(f"Request from {ctx.author.name}. Chefkoch zu viele Zutaten.")
            elif len(options) == 0:
                await ctx.reply("Gib halt wenigstens ne Zutat.")
                logger.info(f"Request from {ctx.author.name}. Chefkoch keine Zutaten.")
            else:
                option = options[0]
                if option == "ROTD" or option == "rotd":
                    recipe = Search().recipeOfTheDay()
                    id = recipe.id
                else:
                    suche = Search(option)
                    recipe = suche.recipes(limit=10)
                    length = len(recipe)
                    random_number = random.randint(0, length)
                    id = recipe[random_number].id
                #print(Recipe(recipe[0]).data_dump())
                adresse = "https://www.chefkoch.de/rezepte/" + id
                await ctx.reply(adresse + "\n" +"SCHMEEECKT :DDD")
                logger.info("Chefkoch für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Request from {ctx.author.name}. Chefkoch.")



def setup(bot):
    bot.add_cog(Chefkoch(bot))
