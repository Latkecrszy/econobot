import discord
import json
import os

from discord.ext import commands, tasks

from PetCog import refreshPets, savePets
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN", None)

bot = commands.Bot(command_prefix="eco!", help_command=None)

bot.remove_command("help")

print("Loading...")


class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


@tasks.loop(seconds=60)
async def feedTrack():
    pets = refreshPets()
    with open("timeLeft.json") as f:
        timeLeft = json.load(f)
    for user, value in timeLeft.items():
        if int(value) == 0:
            member = bot.get_user(id=int(user))
            pet = pets[str(member.id)]
            await member.send(embed=discord.Embed(
                title=f"Your didn't feed {pet.name} for 3 days straight, and it ran out in search of a better life.",
                color=discord.Color.red()))
            pets.pop(str(member.id))
            timeLeft.pop(str(member.id))
            break
        else:
            value = int(value)
            value -= 1
            timeLeft[user] = value
    with open("timeLeft.json", "w") as f:
        json.dump(timeLeft, f, indent=4)
    savePets(pets)


@tasks.loop(seconds=1)
async def idle():
    with open("WordSmithMoney.json", "r") as f:
        player = json.load(f)

    for key, value in player.items():
        amount = round(value["upgrades"] * (1.2 ** value["prestige"]), 2)
        player[str(key)]['money'] += amount
        player[str(key)]['money'] = round(player[str(key)]['money'], 2)
        cost = round(
            (10 * (1.2 ** ((player[str(key)]['upgrades']) - 1))) * (1 - (0.1 * player[str(key)]['couponBook'])), 2)
        pAuto = int(player[str(key)]['autoInvestor'])
        if pAuto > 0 and player[str(key)]['autoInvestor'] == pAuto and player[str(key)]['money'] >= (
                (2.1 - (0.1 * pAuto)) * cost):
            player[str(key)]['money'] -= cost
            player[str(key)]['money'] = round(player[str(key)]['money'], 2)
            player[str(key)]['upgrades'] += 1
        with open("WordSmithMoney.json", "w") as f:
            json.dump(player, f, indent=4)


@bot.event
async def on_ready():
    idle.start()
    feedTrack.start()
    await bot.change_presence(activity=discord.Game(f"Waiting for the next upgrade.", status=discord.Status.online))
    print("Ready")


bot.load_extension("WordSmithBlackJack")
bot.load_extension("WordSmithPlayer")
bot.load_extension("ErrorCog")
bot.load_extension("WordSmithRoulette")
bot.load_extension("WordSmithUtilities")
bot.load_extension("PetCog")
bot.load_extension("idle")
bot.load_extension("HelpCog")

bot.run(TOKEN)

