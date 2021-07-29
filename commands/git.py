from discord.ext import commands
import logging

logger = logging.getLogger("ZicklaaBot.Git")

class Git(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def git(self,ctx):
        try:
            await ctx.channel.send("https://github.com/Zicklaa/Zicklaa-Bot")
            logger.info('Git Link gepostet für ' + ctx.author.name)
        except:
            await ctx.channel.send(
                'Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: git_gud()')
            logger.error('Git von ' + ctx.author.name)


def setup(bot):
    bot.add_cog(Git(bot))