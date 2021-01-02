import discord
from discord.ext import commands
import json


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["invite"])
    async def botinvite(self, ctx):
        await ctx.send(embed=discord.Embed(
            description=f"Click [here](https://discord.com/oauth2/authorize?client_id=758856234446225408&permissions=8&scope=bot) to invite the bot!"))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Connection speed is {int(self.bot.latency * 1000)}ms.")

    @commands.command()
    async def gimmemoney(self, ctx):
        if ctx.author.id == 592503405122027520:
            players = json.load(open("WordSmithMoney.json"))
            players[str(ctx.author.id)]['money'] += 10000
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
            await ctx.send("I gotchu bro, here's $10k \U0001f44d")
        else:
            await ctx.send(f"This command is meant for developers. Sorry!")


def setup(bot):
    bot.add_cog(UtilityCog(bot))