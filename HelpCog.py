import discord
from discord.ext import commands
import json
import random


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
      await ctx.author.send(embed=discord.Embed(description='''***Basic commands (Prefix is eco!)***
 **- eco!start**
    ⠀- Creates an account with the bot
 **- eco!balance/bal/b**
    ⠀- Shows your current balance
 **- eco!give/donate <mention user> <value>**
    ⠀- Gives a certain user money from your balance. 
 **- eco!invite**
    ⠀- Get the link to invite the bot to your server
 **- eco!help** 
    ⠀- Shows the help menu
 **- eco!channel <Channel ID>**
    ⠀- Set the bot to a certain channel
 **- eco!pet help**
    ⠀- Opens the pet specific help menu

***Gambling commands***
 **- eco!blackjack/bj <Wager>**
    ⠀- Initiates a game of blackjack
 **- eco!rps <Rock/Paper/Scissors> <Wager>**
    ⠀- Play rock paper scissors against the bot.
 **- eco!slots <Wager>**
    ⠀- Play with a slot machine
 **- eco!roulette <Wager> <0-35/Red/Black/High/Low/Row 1-3⠀>**
    ⠀- Play roulette

***Idle Commands***
 **- eco!idle**
    ⠀- Shows your current idle stats (Upgrades, Prestige, Achievements, etc.)
 **- eco!upgrade**
    ⠀- Upgrades to the next idle level.
 - eco!prestige
    ⠀- Resets your balance but improves your gameplay 
 **- eco!tokenshop**
    ⠀- Opens the prestige shop
 **- eco!tokenbuy <Upgrade Name>**
    ⠀- Purchases the corresponding prestige upgrade 
  **- eco!togglebuy**
    ⠀- Enables/Disables the automatic buying of upgrades. Must have the Auto Investor Upgrade to unlock.'''))




def setup(bot):
    bot.add_cog(HelpCog(bot))
