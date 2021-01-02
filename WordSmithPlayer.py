import discord
from discord.ext import commands, tasks
import random
from discord.ext.commands.cooldowns import BucketType
import json


class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        if str(ctx.author.id) in players.keys():
            await ctx.send(
                embed=discord.Embed(description=f"An account already exists for {ctx.author.mention}."))
        else:
            players[str(ctx.author.id)] = {"money": 1,
                                           "prestigeTokens": 0,
                                           "items": {"Rocks": 0,
                                                     "Papers": 0,
                                                     "Scissors": 0},
                                           "idle":
                                               {"upgrades": 1,
                                                "prestige": 0,
                                                "couponBook": 0,
                                                "autoInvestor": 0,
                                                "petCare": 0,
                                                "petCareCooldown": 0}}
            embed = discord.Embed(
                description=f"Account created for {ctx.author.mention}.",
                color=discord.Color.green())
            await ctx.send(embed=embed)
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)

    @commands.command(aliases=["Donate", "DONATE", "give", "Give", "GIVE"])
    async def donate(self, ctx, user: discord.Member, money: int):
        if money > 0:
            players = json.load(open("WordSmithMoney.json"))
            if str(user.id) in players.keys():
                if players[str(ctx.author.id)]["money"] >= money:
                    players[str(user.id)]["money"] += money
                    players[str(ctx.author.id)]["money"] -= money
                    await ctx.send(embed=discord.Embed(description=f"${money} has been given to {user.mention}!",
                                                       color=discord.Color.green()))
                else:
                    await ctx.send(embed=discord.Embed(
                        description=f"You do not have enough money to donate {money}{ctx.author.mention}!",
                        color=discord.Color.red()))
            else:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"{user.mention} does not yet have an account {ctx.author.mention}!",
                        color=discord.Color.red()))
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
        else:
            await ctx.send("Error: Donation negative.")

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    async def hourly(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        player = players[str(ctx.author.id)]
        player['money'] += 10
        await ctx.send(embed=discord.Embed(description=f"Hourly claimed {ctx.author.mention}. You gained $10!"))
        json.dump(players, open("WordSmithMoney.json", "w"), indent=4)

    @commands.command(aliases=["bal", "b", "Bal", "BAL", "B", "Balance", "BALANCE"])
    async def balance(self, ctx, member: discord.Member = None):
        players = json.load(open("WordSmithMoney.json"))
        if member is None:
            await ctx.send(embed=discord.Embed(
                description=f"Your balance, {ctx.author.mention}, is ${round((players[str(ctx.author.id)]['money']), 2)}."))
        else:
            if str(member.id) in players.keys():
                await ctx.send(embed=discord.Embed(
                    description=f"{member.display_name} has ${players[str(member.id)]['money']} in their account."))
            else:
                await ctx.send(embed=discord.Embed(
                    description=f"I could not find an account for {member.display_name}, {ctx.author.mention}."))

    @commands.command()
    async def rps(self, ctx, choice, bet):
        players = json.load(open("WordSmithMoney.json"))
        bet = int(bet)
        if players[str(ctx.author.id)]['money'] >= bet:
            choice = choice.lower()
            choices = ["rock", "paper", "scissors"]
            botChoice = random.choice(choices)
            if choice == "rock":
                players[str(ctx.author.id)].rock += 1
            elif choice == "scissors":
                players[str(ctx.author.id)].scissors += 1
            elif choice == "paper":
                players[str(ctx.author.id)].paper += 1
            if choice == botChoice:
                embed = discord.Embed(title=f"We tied! We both chose {choice}!")
            elif choice == "rock" and botChoice == "paper" or choice == "paper" and botChoice == "scissors" or choice == "scissors" and botChoice == "rock":
                embed = discord.Embed(title=f"I won! {botChoice} beats {choice}!", color=discord.Color.green())
                players[str(ctx.author.id)]['money'] -= bet
            elif choice == "rock" and botChoice == "scissors" or choice == "paper" and botChoice == "rock" or choice == "scissors" and botChoice == "paper":
                embed = discord.Embed(title=f"You won! {choice} beats {botChoice}!", color=discord.Color.green())
                players[str(ctx.author.id)]['money'] += bet
            else:
                embed = discord.Embed(
                    title=f"Error: {choice} is not a valid option.")
            await ctx.send(embed=embed)
            if players[str(ctx.author.id)].rock == 500:
                players[str(ctx.author.id)].items["rock"] += 1
                await ctx.send(embed=discord.Embed(
                    description=f"Congrats, {ctx.author.mention}! You have earned a rock collectible.",
                    color=discord.Color.green()))
            elif players[str(ctx.author.id)].paper == 500:
                players[str(ctx.author.id)].items["paper"] += 1
                await ctx.send(embed=discord.Embed(
                    description=f"Congrats, {ctx.author.mention}! You have earned a paper collectible.",
                    color=discord.Color.green()))
            elif players[str(ctx.author.id)].scissors == 500:
                players[str(ctx.author.id)].items["scissors"] = +1
                await ctx.send(embed=discord.Embed(
                    description=f"Congrats, {ctx.author.mention}! You have earned a scissors collectible    .",
                    color=discord.Color.green()))
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)

        else:
            await ctx.send(embed=discord.Embed(
                description=f"Not enough money {ctx.author.mention}! You only have ${players[str(ctx.author.id)]['money']}!"))

    @rps.error
    async def rpserror(self, ctx, error):
        await ctx.send(f"Please use the correct format for this command: `eco!rps rock 100`")

    @commands.command(aliases=["Items", "ITEMS"])
    async def items(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        player = players[str(ctx.author.id)]
        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.author.display_name}'s items:")
        for item, value in player.items.items():
            if value != "none" and value != 0 and value != "0":
                embed.add_field(name=f"{item.name}", value=f"{value} owned.")
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, Items):
        Items = Items.lower()
        players = json.load(open("WordSmithMoney.json"))
        player = players[str(ctx.author.id)]
        for item in player.items.keys():
            if item.name.lower() == Items:
                if item.cost == "none":
                    await ctx.send(embed=discord.Embed(description=f"This item is not for sale, {ctx.author.mention}.",
                                                       color=discord.Color.red()))
                else:
                    if float(player['money']) >= float(item.cost):
                        player.items[item] += 1
                        item.cost = float(item.cost)
                        player['money'] -= item.cost
                        item.cost *= 1.1
                        await ctx.send(
                            embed=discord.Embed(description=f"You have purchased a {item.name} {ctx.author.mention}!",
                                                color=discord.Color.green()))
                    else:
                        await ctx.send(embed=discord.Embed(
                            description=f"You cannot afford to buy this item {ctx.author.mention}! You need ${item.cost}, and you only have ${player['money']}!",
                            color=discord.Color.red()))
        json.dump(players, open("WordSmithMoney.json", "w"), indent=4)


def setup(bot):
    bot.add_cog(PlayerCog(bot))
