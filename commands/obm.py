import logging
import random
from discord.ext import commands
import asyncpraw

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
            reddit = asyncpraw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa",
            )
            memes = await reddit.subreddit("okbrudimongo")
            random_submission = random.choice(
                [meme async for meme in memes.hot(limit=limit)]
            )
            await reddit.close()
            if (
                random_submission.url.endswith("jpg")
                or random_submission.url.endswith("png")
                or random_submission.url.endswith("gif")
                or "v." in random_submission.url
            ):
                await ctx.channel.send("|| " + random_submission.url + " ||")
                if "imgur" in random_submission.url:
                    await ctx.channel.send("imgur 🤮")
                await ctx.message.delete()
                logger.info("Redditlink gepostet für: " + ctx.author.name)
            else:
                await ctx.reply(
                    "Comment oder Gallery Post erwischt, probier es nochmal :^)"
                )
                logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

        except Exception as e:
            await reddit.close()
            logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

    @commands.command()
    async def oow(self, ctx):
        try:
            reddit = asyncpraw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa",
            )
            memes = await reddit.subreddit("okoidawappler")
            random_submission = random.choice(
                [meme async for meme in memes.hot(limit=limit)]
            )
            await reddit.close()
            if (
                random_submission.url.endswith("jpg")
                or random_submission.url.endswith("png")
                or random_submission.url.endswith("gif")
                or "v." in random_submission.url
            ):
                await ctx.channel.send("|| " + random_submission.url + " ||")
                if "imgur" in random_submission.url:
                    await ctx.channel.send("imgur 🤮")
                await ctx.message.delete()
                logger.info("Redditlink gepostet für: " + ctx.author.name)
            else:
                await ctx.reply(
                    "Comment oder Gallery Post erwischt, probier es nochmal :^)"
                )
                logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

        except Exception as e:
            await reddit.close()
            logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

    @commands.command()
    @commands.check(is_hallo_anna)
    async def ali(self, ctx):
        try:
            reddit = asyncpraw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa",
            )
            memes = await reddit.subreddit("kpopfap")
            random_submission = random.choice(
                [meme async for meme in memes.hot(limit=limit)]
            )
            await reddit.close()
            if (
                random_submission.url.endswith("jpg")
                or random_submission.url.endswith("png")
                or random_submission.url.endswith("gif")
                or "gfycat" in random_submission.url
            ):
                await ctx.channel.send("|| " + random_submission.url + " ||")
                if "imgur" in random_submission.url:
                    await ctx.channel.send("imgur 🤮")
                await ctx.message.delete()
                logger.info("Redditlink gepostet für: " + ctx.author.name)
            else:
                await ctx.reply(
                    "Comment oder Gallery Post erwischt, probier es nochmal :^)"
                )
                logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

        except Exception as e:
            await reddit.close()
            logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

    @commands.command()
    async def obr(self, ctx):
        try:
            reddit = asyncpraw.Reddit(
                client_id=self.bot.CLIENT_ID,
                client_secret=self.bot.CLIENT_SECRET,
                user_agent="by u/zicklaa",
            )
            memes = await reddit.subreddit("okbuddyretard")
            random_submission = random.choice(
                [meme async for meme in memes.hot(limit=limit)]
            )
            await reddit.close()
            if (
                random_submission.url.endswith("jpg")
                or random_submission.url.endswith("png")
                or random_submission.url.endswith("gif")
                or "v." in random_submission.url
            ):
                await ctx.channel.send("|| " + random_submission.url + " ||")
                if "imgur" in random_submission.url:
                    await ctx.channel.send("imgur 🤮")
                await ctx.message.delete()
                logger.info("Redditlink gepostet für: " + ctx.author.name)
            else:
                await ctx.reply(
                    "Comment oder Gallery Post erwischt, probier es nochmal :^)"
                )
                logger.error(f"OBM ERROR von {ctx.author.name}: {e}")

        except Exception as e:
            await reddit.close()
            logger.error(f"OBM ERROR von {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Okbrudimongo(bot))
