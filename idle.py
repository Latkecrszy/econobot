import discord
from discord.ext import commands
import json
from discord.ext.commands.cooldowns import BucketType
import random


class IdleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def upgrade(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        player = players[str(ctx.author.id)]
        costUpgrade = round((10 * (1.2 ** ((player['upgrades']) - 1))) * (1 - (0.1 * player['couponBook'])), 2)
        if player['money'] >= costUpgrade:
            player["upgrades"] += 1
            player['money'] -= costUpgrade
            costUpgrade = round((10 * (1.2 ** ((player['upgrades']) - 1))) * (1 - (0.1 * player['couponBook'])), 2)
            await ctx.send(
                f"Level increased to {player['upgrades']}, {ctx.author.mention}. The next upgrade will cost ${costUpgrade}")
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
        else:
            await ctx.send(
                f"You do not have enough money to upgrade! You have ${player['money']}, and you need ${costUpgrade}!")

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def prestige(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        player = players[str(ctx.author.id)]
        costPrestige = round((0.2e7 ** player["prestige"] + 1e7), 2)
        if player['money'] >= costPrestige:
            player["prestige"] += 1
            player["upgrades"] = 1
            player['money'] = 0
            player['prestigeTokens'] += 1
            await ctx.send(
                f"You've risen to Prestige {player['prestige']}, and have gained a prestige token. Do eco!token to spend it.")
            players[str(ctx.author.id)] = player
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
        else:
            await ctx.send(
                f"You do not have enough money to prestige! You have ${round(player['money'], 2)}, and you need ${costPrestige}!")

    @commands.command()
    async def togglebuy(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        player = players[str(ctx.author.id)]
        if player['autoInvestor'] > 0:
            if player['autoInvestor'] == int(player['autoInvestor']):
                players[str(ctx.author.id)]['autoInvestor'] += 0.1
                await ctx.send(embed=discord.Embed(description=f"You have disabled your AutoInvestor",
                                                   color=discord.Color.green()))
            else:
                players[str(ctx.author.id)]['autoInvestor'] -= 0.1
                await ctx.send(
                    embed=discord.Embed(description=f"You have enabled your AutoInvestor", color=discord.Color.green()))
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)

    @commands.command()
    async def idle(self, ctx):
        player = json.load(open("WordSmithMoney.json"))[str(ctx.author.id)]
        pMoney = player['money']
        pUpgrades = player['upgrades']
        pPrestige = player['prestige']
        pTokens = player['prestigeTokens']
        pAutoInvestor = int(player['autoInvestor'])
        pCouponBook = player['couponBook']
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Idle stats")
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"Money: ", value=str(pMoney))
        embed.add_field(name=f"Level: ", value=str(pUpgrades))
        embed.add_field(name=f"Times prestiged: ", value=str(pPrestige))
        if pPrestige > 0:
            embed.add_field(name=f"Prestige Tokens: ", value=str(pTokens))
            embed.add_field(name=f"Auto Investor Level: ", value=str(int(pAutoInvestor)))
            embed.add_field(name=f"Coupon Book Level: ", value=str(pCouponBook))
        await ctx.send(embed=embed)

    @commands.command()
    async def tokenshop(self, ctx):
        player = json.load(open("WordSmithMoney.json"))[str(ctx.author.id)]
        pAutoInvestor = int(player['autoInvestor'])
        pCouponBook = player['couponBook']
        pPetCare = player['petCare']
        tokenshop = [
            {"name": f"Auto Investor {pAutoInvestor + 1}",
             "description": f"Buys the next upgrade when available, toggle with eco!autobuy. (Note: Requires a {200 - (20 * pAutoInvestor)}% buffer.",
             "price": int(1 + 0.5 * pAutoInvestor)},
            {"name": f"Coupon Book {pCouponBook + 1}", "price": int(1 + 0.5 * pCouponBook),
             "description": f"Allows you to buy upgrades for {10 * (pCouponBook + 1)}% less."},
            {"name": "Pet Care 1", "price": 1,
             "description": "Will automatically feed your pet if you go 3 days without feeding them. Only works once a week."},
            {"name": "Pet Care 2", "price": 1,
             "description": "Your pets become more self-sufficent, and can go 4 days without eating."},
            {"name": "Pet Care 3", "price": 2, "description": "Earn double XP and money from fetch, dig, and play."},
            {"name": "Pet Care 4", "price": 2,
             "description": "Your pets learn to feed themselves.  They no longer need to eat."},
            {"name": "Pet Care 5", "price": 3, "description": "Triple XP and money from fetch, dig, and play."}]
        embed = discord.Embed(title="Prestige Shop")
        for item in tokenshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            if "Auto Investor" in name:
                if pAutoInvestor <= 4:
                    embed.add_field(name=name, value=f"{price} tokens | {desc}")
            elif "Coupon Book" in name:
                if pCouponBook <= 4:
                    embed.add_field(name=name, value=f"{price} tokens | {desc}")
        await ctx.send(embed=embed)

    @commands.command()
    async def tokenbuy(self, ctx, *, pUpgrade):
        pUpgrade = pUpgrade.lower()
        players = json.load(open("WordSmithMoney.json"))
        player = players[str(ctx.author.id)]
        pAutoInvestor = int(player['autoInvestor'])
        pCouponBook = player['couponBook']
        pPetCare = player['petCare']
        pTokens = player['prestigeTokens']
        if "auto investor" in str(pUpgrade):
            if pAutoInvestor < 5:
                cost = int(1 + 0.5 * pAutoInvestor)
                if cost <= pTokens:
                    players[str(ctx.author.id)]['prestigeTokens'] -= cost
                    players[str(ctx.author.id)]['autoInvestor'] += 1
                    await ctx.send(embed=discord.Embed(
                        description=f"You have upgraded your Auto Investor to level {pAutoInvestor + 1}!",
                        color=discord.Color.green()))
                    json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
                else:
                    await ctx.send(
                        embed=discord.Embed(description=f"You need {cost - pTokens} more token(s) to purchase this.",
                                            color=discord.Color.red()))
            else:
                await ctx.send(embed=discord.Embed(description="You have already maxed out the Auto Investor.",
                                                   color=discord.Color.red()))
        elif "pet care" in str(pUpgrade):
            if pPetCare < 5:
                cost = int(1 + 0.5 * pPetCare)
                if cost <= pTokens:
                    if 0:
                        players[str(ctx.author.id)]['prestigeTokens'] -= cost
                        players[str(ctx.author.id)]['petCare'] += 1
                        await ctx.send(
                            embed=discord.Embed(description=f"You have upgraded your Pet Care to level {pPetCare + 1}!",
                                                color=discord.Color.green()))
                        json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
                    else:
                        await ctx.send(
                            embed=discord.Embed(description=f"This stuff isn't in yet. Please wait until then",
                                                color=discord.Color.green()))
                else:
                    await ctx.send(
                        embed=discord.Embed(description=f"You need {cost - pTokens} more token(s) to purchase this.",
                                            color=discord.Color.red()))
            else:
                await ctx.send(embed=discord.Embed(description="You have already maxed out the Pet Care.",
                                                   color=discord.Color.red()))
        elif "coupon book" in str(pUpgrade):
            if pCouponBook < 5:
                cost = int(1 + 0.5 * pCouponBook)
                if cost <= pTokens:
                    players[str(ctx.author.id)]['prestigeTokens'] -= cost
                    players[str(ctx.author.id)]['couponBook'] += 1
                    await ctx.send(
                        embed=discord.Embed(description=f"You have upgraded your Pet Care to level {pCouponBook + 1}!",
                                            color=discord.Color.green()))
                    json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
                else:
                    await ctx.send(
                        embed=discord.Embed(description=f"You need {cost - pTokens} more token(s) to purchase this.",
                                            color=discord.Color.red()))
            else:
                await ctx.send(embed=discord.Embed(description="You have already maxed out the Coupon Book.",
                                                   color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(
                description='That is not a valid option. Please choose between "Coupon Book", "Auto Investor", and "Pet Care"'))


def setup(bot):
    bot.add_cog(IdleCog(bot))
