import logging
from datetime import datetime

from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Wishlist")


async def can_delete(ctx):
    return (
        ctx.author.id == 288413759117066241
        or ctx.author.id == 156136437887008771
        or ctx.author.id == 136103007065473024
    )


class Wishlist(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.cursor = db.cursor()

    @commands.hybrid_command()
    async def wishlist(self, ctx, *wishtext):
        try:
            if len(wishtext) < 1:
                try:
                    self.cursor.execute("SELECT * FROM wishlist")
                    wishes = self.cursor.fetchall()
                    if not wishes:
                        await ctx.channel.send("Ihr seid wunschlos glücklich :3")
                        logger.info("Wishlist: Leer für " + ctx.author.name)
                    else:
                        all_wishes = "Folgendes wünscht ihr euch: \n\n"
                        x = 1
                        for wish in wishes:
                            all_wishes = (
                                all_wishes + "ID: " + str(wish[0]) + ": " + "\n"
                            )
                            all_wishes = all_wishes + "**" + wish[2] + "**" + "\n"
                            all_wishes = (
                                all_wishes
                                + "<@"
                                + str(wish[1])
                                + ">"
                                + " ("
                                + wish[3]
                                + ")"
                                + "\n"
                                + "\n"
                            )
                            x = x + 1
                        if len(all_wishes) > 1999:
                            
                            substrings = []

                            for i in range(0, len(all_wishes), 2000):
                                substring = all_wishes[i:i + 2000]
                                substrings.append(substring)
                            for substring in substrings:
                                await ctx.channel.send(substring)
                            logger.info(
                                "Wishlist: Geteilte Liste gepostet für "
                                + ctx.author.name
                            )
                        else:
                            await ctx.channel.send(all_wishes)
                        logger.info("Wishlist: Liste gepostet für " + ctx.author.name)
                except Exception as e:
                    await ctx.channel.send(
                        "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: showlist()"
                    )
                    logger.error("showlist: " + ctx.author.name + ": " + e)
            else:
                wishtext_join = " ".join(wishtext)
                if len(wishtext_join) < 250:
                    user_id = ctx.author.id
                    ts = datetime.now().strftime("%d-%b-%Y | %H:%M:%S")
                    sql = (
                        "INSERT INTO wishlist (user_id, wishtext, ts) VALUES (?, ?, ?)"
                    )
                    val = (user_id, wishtext_join, ts)
                    self.cursor.execute(sql, val)
                    self.db.commit()
                    await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
                    logger.info("Wishlist: neuer Wunsch + Reaktion")
                else:
                    await ctx.channel.send("Wunsch zu lang, maximal 250 Chars.")
                    logger.info("Wishlist: Wunsch zu lang von " + ctx.author.name)
        except Exception as e:
            await ctx.channel.send(
                "Irgendwas klappt nedde. Scheiß Zicklaa zsamme gschwind. Hint: wishlist()"
            )
            logger.error(ctx.author.name + ": " + str(e))

    @commands.hybrid_command()
    @commands.check(can_delete)
    async def delwish(self, ctx, id):
        try:
            try:
                intid = int(id)
            except:
                await ctx.channel.send("Die ID sollte schon ne Zahl sein")
                return
            self.cursor.execute("SELECT * FROM wishlist WHERE id=?", (intid,))
            wish = self.cursor.fetchall()
            if not wish:
                await ctx.channel.send("Ein Wunsch mit der ID gibts nedde")
                logger.info("delete_wish: Wish beim Löschen nicht gefunden")
            else:
                self.cursor.execute("DELETE FROM wishlist WHERE id=?", (intid,))
                self.db.commit()
                await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
                logger.info("delete_wish: Wish gelöscht mit der ID: " + id)
        except Exception as e:
            await ctx.channel.send("Irgendwas stimmt mit der ID nicht, Mois")
            logger.error("delete_wish: Fehler bei Eingabe der ID: " + e)

    @delwish.error
    async def delwish_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Gib eine ID an oder so, Lan")
            logger.error("delete_wish: Keine ID von " + ctx.author.name)


async def setup(bot):
    await bot.add_cog(Wishlist(bot, bot.db))
