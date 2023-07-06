import logging
import random
import discord
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Girlboss")


girlboss_list = [
    "You go Girl!",
    "Du schaffst das!",
    "Ich glaub an dich!",
    "Halte durch!",
    "Slay Queen!",
    "Gaslight, Gatekeep, Girlboss!",
    "Du bist eine starke und eigenständige Frau!",
    "Ich bin so stolz auf deine Erfolge und Fortschritte!",
    "#BossQueen",
    "Wer kämpft, kann verlieren. Wer nicht kämpft, hat schon verloren.",
    "Es ist immer zu früh, um aufzugeben.",
    "Jede schwierige Situation, die du jetzt meisterst, bleibt dir in der Zukunft erspart.",
    "Wenn Du etwas gesagt haben willst frage einen Mann; wenn Du etwas getan haben willst frage eine Frau.",
    "Das Leben ist hart, aber das bist du auch.",
    "Habt keine Angst, für dich selbst einzutreten. Kämpfe weiter für deine Träume!",
    "Vergiss niemals deinen eigenen Wert!",
    "Jeder Tag ist dein Tag!",
    "Alles ist möglich wenn du nur wirklich willst!",
]
girlbosses = (200009451292459011, 134574105109331968, 288413759117066241)


class Girlboss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def girlboss(self, ctx):
        try:
            if int(ctx.author.id) in girlbosses:
                text = random.choice(girlboss_list)
                await ctx.reply(f"<@{int(ctx.author.id)}> {text}")
                logger.info("Girlboss gepostet für " + ctx.author.name)
            else:
                await ctx.reply("Nur Mariam und Wursti tun Girlbossen tun >:(")
                logger.info("Girlboss für " + ctx.author.name)
        except Exception as e:
            await ctx.reply("Heute kein Girlbossen :/")
            logger.error(f"Girlboss Error from {ctx.author.name}: {e}")


def setup(bot):
    bot.add_cog(Girlboss(bot))
