import logging

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Git")


class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def git(self, ctx):
        try:
            await ctx.reply("https://github.com/Zicklaa/Zicklaa-Bot")
            logger.info("Git Link gepostet für " + ctx.author.name)
        except Exception as e:
            await ctx.reply(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: git_gud()"
            )
            logger.error(f"Request from {ctx.author.name}: {e}")


async def setup(bot):
    await bot.add_cog(Git(bot))
