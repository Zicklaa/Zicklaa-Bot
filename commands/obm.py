import logging
import os
import random
import discord
import config
from discord.ext import commands
import praw

logger = logging.getLogger("ZicklaaBot.Okbrudimongo")

limit = 25


class Okbrudimongo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def obm(self, ctx):
        try:
            reddit = praw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa"
            )
            random_submission = reddit.subreddit('okbrudimongo').random()
            await ctx.reply(random_submission.url)
            '''submissions = [submission for submission in reddit.subreddit("okbrudimongo").hot(limit=limit)]
            await ctx.reply(submissions[random.randint(0, limit)].url)'''
            logger.info("Redditlink gepostet für: " + ctx.author.name)

        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

    @commands.command()
    async def oow(self, ctx):
        try:
            reddit = praw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa"
            )
            random_submission = reddit.subreddit('okoidawappler').random()
            await ctx.reply(random_submission.url)
            '''submissions = [submission for submission in reddit.subreddit("okoidawappler").hot(limit=limit)]
            await ctx.reply(submissions[random.randint(0, limit)].url)'''
            logger.info("Redditlink gepostet für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"OOW ERROR von {ctx.author.name}: {e}")

    @commands.command()
    async def obr(self, ctx):
        try:
            reddit = praw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa"
            )
            submissions = [submission for submission in reddit.subreddit(
                "okbuddyretard").hot(limit=limit)]
            await ctx.reply(submissions[random.randint(0, limit)].url)
            logger.info("Redditlink gepostet für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"OBR ERROR von {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Okbrudimongo(bot))
