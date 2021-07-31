import logging

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Admin")


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_privileged(ctx):
        return (ctx.author.guild_permissions.administrator or ctx.author.id == 136103007065473024
        or ctx.author.id == 288413759117066241 or ctx.author.id == 156136437887008771)

    @commands.command(hidden=True)
    @commands.check(is_privileged)
    async def load(self, ctx, extension_name: str):
        try:
            self.bot.load_extension(f"commands.{extension_name}")
        except Exception as e:
            await ctx.send("```\n{}: {}\n```".format(type(e).__name__, str(e)))
            logger.error("{}: {}".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.check(is_privileged)
    async def unload(self, ctx, extension_name: str):
        self.bot.unload_extension(f"commands.{extension_name}")
        await ctx.send("{} unloaded.".format(extension_name))


def setup(bot):
    bot.add_cog(Admin(bot))
