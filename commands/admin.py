import asyncio
import logging

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Admin")


async def is_privileged(ctx):
    return (
        ctx.author.guild_permissions.administrator
        or ctx.author.id == 136103007065473024
        or ctx.author.id == 288413759117066241
        or ctx.author.id == 156136437887008771
    )


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(hidden=True)
    @commands.check(is_privileged)
    async def load(self, ctx, extension_name: str):
        try:
            self.bot.load_extension(f"commands.{extension_name}")
        except Exception as e:
            await ctx.send("```\n{}: {}\n```".format(type(e).__name__, str(e)))
            logger.error("{}: {}".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))

    @commands.hybrid_command(hidden=True)
    @commands.check(is_privileged)
    async def unload(self, ctx, extension_name: str):
        self.bot.unload_extension(f"commands.{extension_name}")
        await ctx.send("{} unloaded.".format(extension_name))

    @commands.hybrid_command(hidden=True)
    @commands.check(is_privileged)
    async def reload(self, ctx, extension_name: str):
        self.bot.unload_extension(f"commands.{extension_name}")
        await asyncio.sleep(2)
        try:
            self.bot.load_extension(f"commands.{extension_name}")
        except Exception as e:
            await ctx.send("```\n{}: {}\n```".format(type(e).__name__, str(e)))
            logger.error("{}: {}".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} reloaded.".format(extension_name))


async def setup(bot):
    await bot.add_cog(Admin(bot))
