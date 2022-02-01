import logging
import os
import random
import discord
import config
from discord.ext import commands
import praw

logger = logging.getLogger("ZicklaaBot.Okbrudimongo")

limit = 50


async def is_hallo_anna(ctx):
    return ctx.channel.id == 528742785935998979

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
            if random_submission.url.endswith("jpg") or random_submission.url.endswith("png") or random_submission.url.endswith("gif"):
                await ctx.channel.send(random_submission.url)
                if 'imgur' in random_submission.url:
                    await ctx.channel.send('imgur 🤮')
                await ctx.message.delete()
                '''submissions = [submission for submission in reddit.subreddit("okbrudimongo").hot(limit=limit)]
                await ctx.reply(submissions[random.randint(0, limit)].url)'''
                logger.info("Redditlink gepostet für: " + ctx.author.name)
            else:
                random_submission = reddit.subreddit('okbrudimongo').random()
                if random_submission.url.endswith("jpg") or random_submission.url.endswith("png") or random_submission.url.endswith("gif"):
                    await ctx.channel.send(random_submission.url)
                    if 'imgur' in random_submission.url:
                        await ctx.channel.send('imgur 🤮')
                    await ctx.message.delete()
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
            if random_submission.url.endswith("jpg") or random_submission.url.endswith("png") or random_submission.url.endswith("gif"):
                await ctx.channel.send(random_submission.url)
                if 'imgur' in random_submission.url:
                    await ctx.channel.send('imgur 🤮')
                await ctx.message.delete()
                '''submissions = [submission for submission in reddit.subreddit("okbrudimongo").hot(limit=limit)]
                await ctx.reply(submissions[random.randint(0, limit)].url)'''
                logger.info("Redditlink gepostet für: " + ctx.author.name)
            else:
                random_submission = reddit.subreddit('okoidawappler').random()
                if random_submission.url.endswith("jpg") or random_submission.url.endswith("png") or random_submission.url.endswith("gif"):
                    await ctx.channel.send(random_submission.url)
                    if 'imgur' in random_submission.url:
                        await ctx.channel.send('imgur 🤮')
                    await ctx.message.delete()
                    '''submissions = [submission for submission in reddit.subreddit("okbrudimongo").hot(limit=limit)]
                    await ctx.reply(submissions[random.randint(0, limit)].url)'''
                    logger.info("Redditlink gepostet für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"OOW ERROR von {ctx.author.name}: {e}")

    @commands.command()
    @commands.check(is_hallo_anna)
    async def ali(self, ctx):
        try:
            reddit = praw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa"
            )
            submissions = [submission for submission in reddit.subreddit(
                "kpopfap").hot(limit=limit)]
            url = submissions[random.randint(0, limit)].url
            if "gallery" in url:
                submissions = [submission for submission in reddit.subreddit(
                    "kpopfap").hot(limit=limit)]
                url = submissions[random.randint(0, limit)].url
                if "gallery" in url:
                    submissions = [submission for submission in reddit.subreddit(
                        "kpopfap").hot(limit=limit)]
                    url = submissions[random.randint(0, limit)].url
                    if "gallery" in url:
                        submissions = [submission for submission in reddit.subreddit(
                            "kpopfap").hot(limit=limit)]
                        url = submissions[random.randint(0, limit)].url
                        await ctx.reply("Nur Galleries ey smh")
                    else:
                        await ctx.reply(url)
                else:
                    await ctx.reply(url)
            else:
                await ctx.reply(url)
            logger.info("Redditlink gepostet für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"OBR ERROR von {ctx.author.name}: {e}")

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
            url = submissions[random.randint(0, limit)].url
            await ctx.reply(url)
            logger.info("Redditlink gepostet für: " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"OBR ERROR von {ctx.author.name}: {e}")

def setup(bot):
    bot.add_cog(Okbrudimongo(bot))
