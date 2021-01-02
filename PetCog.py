import discord
from discord.ext import commands
import json
import random
from discord.ext.commands.cooldowns import BucketType


def savePets(pets):
    for player, pet in pets.items():
        pets[player] = [pet.name, pet.type, str(pet.xp), str(pet.level)]
    with open("pets.json", "w") as a:
        json.dump(pets, a, indent=4)


def refreshPets():
    with open("pets.json", "r") as f:
        pets = json.load(f)
    for key, value in pets.items():
        pets[key] = Pet(value[0], value[1], value[2], value[3])
    return pets


class Pet(commands.Cog):
    def __init__(self, name, Type, xp, level):
        self.name = name
        self.type = Type
        self.xp = xp
        self.level = level

    @commands.command()
    async def viewpet(self, ctx):
        pets = refreshPets()
        if str(ctx.author.id) in pets.keys():
            pet = pets[str(ctx.author.id)]
            embed = discord.Embed(title=f"{pet.name} the {pet.type}:")
            embed.set_author(name=f"{ctx.author}'s pet", icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"Experience: ", value=str(pet.xp))
            embed.add_field(name=f"Level: ", value=str(pet.level))
            await ctx.send(embed=embed)
            savePets(pets)
        else:
            await ctx.send(embed=discord.Embed(description=f"You do not yet have a pet {ctx.author.mention}!",
                                               color=discord.Color.red()))

    @commands.group()
    async def pet(self, ctx):
        pass

    @pet.command()
    async def help(self, ctx):
        embed = discord.Embed(title=f"Pet Help:", color=discord.Color.green())
        embed.add_field(name=f"Pet list:",
                        value="turtle\nPrice: $500,000\ndog\nPrice: $500,000\ncat\nPrice: $500,000\nrock\nPrice: $500,000\nparrot\nPrice: $2,500,000\nlizard\nPrice: $2,500,000\naxolotl\nPrice: $2,500,000\nrock with googly eyes\nPrice: $2,500,000\n")
        embed.add_field(name="Games:", value="fetch\ndig\nplay\nfeed")
        embed.add_field(name="Commands:",
                        value="eco!pet feed\neco!pet play\neco!pet fetch\neco!pet dig\neco!viewpet\neco!buypet <name> <species>")
        await ctx.send(embed=embed)

    @pet.command()
    async def view(self, ctx):
        pets = refreshPets()
        if str(ctx.author.id) in pets.keys():
            pet = pets[str(ctx.author.id)]
            embed = discord.Embed(title=f"{pet.name} the {pet.type}:")
            embed.set_author(name=f"{ctx.author}'s pet", icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"Experience: ", value=str(pet.xp))
            embed.add_field(name=f"Level: ", value=str(pet.level))
            await ctx.send(embed=embed)
            savePets(pets)
        else:
            await ctx.send(embed=discord.Embed(description=f"You do not yet have a pet {ctx.author.mention}!",
                                               color=discord.Color.red()))

    @pet.command()
    async def feed(self, ctx):
        pets = refreshPets()
        pet = pets[str(ctx.author.id)]
        with open("timeLeft.json") as f:
            timeLeft = json.load(f)
        with open("WordSmithMoney.json") as f:
            players = json.load(f)
        petCare = players[str(ctx.author.id)]["petCare"]
        if petCare > 1 and petCare < 4:
            timeLeft[str(ctx.author.id)] = 5760
        elif petCare < 2:
            timeLeft[str(ctx.author.id)] = 4320
        with open("timeLeft.json", "w") as f:
            json.dump(timeLeft, f, indent=4)
        await ctx.send(embed=discord.Embed(title=f"{pet.name} the {pet.type} has been fed.",
                                           color=discord.Color.green()))

    @pet.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def fetch(self, ctx):
        pets = refreshPets()
        pet = pets[str(ctx.author.id)]
        pet.xp = int(pet.xp)
        levelUp = int(pet.level) * 100
        newXP = random.randint(int(levelUp / 100), int(levelUp / 20))
        pet.xp += int(newXP * 10)
        await ctx.send(
            f"Your pet successfully fetched... whatever it was you threw for them! {pet.name} the {pet.type} just gained {newXP * 10} XP {ctx.author.mention}!")
        if pet.xp >= int(pet.level) * 1000:
            pet.xp = 0
            pet.level = int(pet.level)
            pet.level += 1
            await ctx.send(
                f"{pet.name} the {pet.type} is now at level {pet.level} {ctx.author.mention}! You will now receive $250 more per day!")
        savePets(pets)

    @pet.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def dig(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        pets = refreshPets()
        pet = pets[str(ctx.author.id)]
        money = random.randint(1000, 5000)
        player = players[str(ctx.author.id)]
        player['money'] += money
        await ctx.send(f"{pet.name} dug up ${money} for you!")
        json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
        savePets(pets)

    @pet.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def play(self, ctx):
        players = json.load(open("WordSmithMoney.json"))
        pets = refreshPets()
        pet = pets[str(ctx.author.id)]
        gain = random.choice(["xp", "money"])
        if gain == "xp":
            pet.xp = int(pet.xp)
            levelUp = int(pet.level) * 100
            newXP = random.randint(int(levelUp / 100), int(levelUp / 20))
            pet.xp += int(newXP * 10)
            await ctx.send(
                f"You played with your pet, and {pet.name} the {pet.type} gained {newXP * 10} XP!")
            if pet.xp >= int(pet.level) * 1000:
                pet.xp = 0
                pet.level = int(pet.level)
                pet.level += 1
                await ctx.send(
                    f"{pet.name} the {pet.type} is now at level {pet.level} {ctx.author.mention}! You will now receive $250 more per day!")
            savePets(pets)
        elif gain == "money":
            money = random.randint(1000, 5000)
            player = players[str(ctx.author.id)]
            player['money'] += money
            await ctx.send(f"You played with your pet, and {pet.name} found ${money} for you!")
            json.dump(players, open("WordSmithMoney.json", "w"), indent=4)
            savePets(pets)

    @pet.command(aliases=["abandon"])
    async def disown(self, ctx):
        pets = refreshPets()
        pet = pets[str(ctx.author.id)]
        pets.pop(str(ctx.author.id))
        with open("timeLeft.json") as f:
            timeLeft = json.load(f)
        timeLeft.pop(str(ctx.author.id))
        with open("timeLeft.json", "w") as f:
            json.dump(timeLeft, f, indent=4)
        await ctx.send(embed=discord.Embed(
            title=f'Your pet, {pet.name}, runs away after you "accidentally" leave the door open.',
            color=discord.Color.red()))
        savePets(pets)

    @pet.command()
    async def rename(self, ctx, *, newName):
        pets = refreshPets()
        pet = pets[str(ctx.author.id)]
        pet.name = newName
        await ctx.send(f"Your pet has been renamed to {pet.name}, {ctx.author.mention}!")
        savePets(pets)

    @commands.command()
    async def buypet(self, ctx, name, *, Type):
        players = json.load(open("WordSmithMoney.json"))
        pets = refreshPets()
        types = ["turtle", "dog", "cat", "rock"]
        expensiveTypes = ["parrot", "lizard", "axolotl", "googly eye rock"]
        if str(ctx.author.id) not in pets.keys():
            if Type.lower() in types:
                if int(players[str(ctx.author.id)]['money']) >= 100000:
                    players[str(ctx.author.id)]['money'] -= 100000
                    pets[str(ctx.author.id)] = Pet(name, Type, 0, 1)
                    savePets(pets)
                    embed = discord.Embed(
                        description=f"You now own a pet {Type} named {name}! Do `eco!pet help` to find out fun things to do with your pet!\nDon't forget to use `eco!pet feed` at least every 3 days so your pet doesn't die!",
                        color=discord.Color.green())
                    with open("timeLeft.json") as f:
                        timeLeft = json.load(f)
                    timeLeft[str(ctx.author.id)] = 4320
                    with open("timeLeft.json", "w") as f:
                        json.dump(timeLeft, f, indent=4)
                else:
                    embed = discord.Embed(
                        description=f"You do not have enough money to purchase a {Type} {ctx.author.mention}!",
                        color=discord.Color.red())
            elif Type.lower() in expensiveTypes:
                if int(players[str(ctx.author.id)]['money']) >= 2500000:
                    players[str(ctx.author.id)]['money'] -= 2500000
                    pets[str(ctx.author.id)] = Pet(name, Type, 0, 1)
                    savePets(pets)
                    embed = discord.Embed(
                        description=f"You now own a pet {Type} named {name}! Do `eco!pet help` to find out fun things to do with your pet!",
                        color=discord.Color.green())
                    with open("timeLeft.json") as f:
                        timeLeft = json.load(f)
                    timeLeft[str(ctx.author.id)] = 4320
                    with open("timeLeft.json", "w") as f:
                        json.dump(timeLeft, f, indent=4)
                else:
                    embed = discord.Embed(
                        description=f"You do not have enough money to purchase a {Type} {ctx.author.mention}!",
                        color=discord.Color.red())
            else:
                embed = discord.Embed(
                    description=f"Please specify a valid type {ctx.author.mention}! Valid types are turtle, dog, cat, rock, parrot, lizard, axolotl, or googly eye rock!!",
                    color=discord.Color.red())
        else:
            embed = discord.Embed(
                description=f"You already own a pet {pets[str(ctx.author.id)].type} {ctx.author.mention}!")
        await ctx.send(embed=embed)
        json.dump(players, open("WordSmithMoney.json", "w"), indent=4)


def setup(bot):
    bot.add_cog(Pet("none", "none", "none", "none"))

