import logging

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Git")


class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def git(self, ctx):
        async with ctx.channel.typing():
            try:
                await ctx.reply("https://github.com/Zicklaa/Zicklaa-Bot")
                logger.info('Git Link gepostet für ' + ctx.author.name)
            except:
                await ctx.reply(
                    'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: git_gud()')
                logger.error('Git von ' + ctx.author.name)


def setup(bot):
    bot.add_cog(Git(bot))
