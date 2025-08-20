        
import logging

import discord
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Threads") 
 
class Threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def join(self, ctx, channel_id: int):
        
        if channel_id is None:
            await ctx.send("Wie denn ohne Channel ID du Grüner???.")
            logger.info(f"Threads: Keine ID gegeben.")
            return
        
        # Fetch the thread by ID
        channel = await self.bot.fetch_channel(channel_id)
        for thread in channel.threads:
            try:
                await thread.join()
                await ctx.send(f"Thread angeschlossen: {thread.name}")
                logger.info(f"Thread angeschlossen: {thread.name}")
            except Exception as e:
                await ctx.send(f"Konnte den Thread nicht anschließen: {thread.name}, Error: {str(e)}")
                logger.error(f"Konnte den Thread nicht anschließen: {thread.name}, Error: {str(e)}")
            

async def setup(bot):
    await bot.add_cog(Threads(bot))
