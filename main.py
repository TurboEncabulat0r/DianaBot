import discord
from discord.ext import commands
import hypixleimpl
import asyncio
import json



bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

discToken = "MTM4MzYwNzY2NDczODgyODI4OQ.GNi5Or.LrFy9sxRkCgLasv5CZdKCySEeJyPUf7D2D8lwI"

dmUsers = []

@bot.slash_command(name="getnotifs")
async def getnotifs(ctx):
    if ctx.author.id not in dmUsers:
        await ctx.author.send("You have been added to the list of users to receive notifications.")
        dmUsers.append(ctx.author.id)
    else:
        await ctx.author.send("You are already on the list of users to receive notifications.")

@bot.slash_command(name="getmayor")
async def getmayor(ctx):
    mayorData = hypixleimpl.getMayorData()
    embed = discord.Embed(title="Current Mayor", description=f"The current mayor is {mayorData['mayor']['name']}")
    await ctx.send(embed=embed)
    print(mayorData)


@bot.slash_command(name="savedata", guild_ids=[1256697556377796658])
async def saveData(ctx):
    electionData = hypixleimpl.getMayorData()
    with open("electionData.json", "w") as f:
        json.dump(electionData, f, indent=4)

@bot.slash_command(name="dianaevent")
async def dianaEvent(ctx):
    electionData = hypixleimpl.getMayorData()
    candidates = electionData["current"]["candidates"]
    for i in range(len(candidates)):
        if candidates[i]["name"] == "Jerry":
            await ctx.send(f"Jerry is running for mayor!")

        if candidates[i]["name"] == "Diana":
            perks = candidates[i]["perks"]

            for j in range(len(perks)):

                if perks[j]["name"] == "Mythological Ritual":
                    await ctx.send(f"Diana is running for mayor!")
                    break

        

async def dmUsers(message):
    for user in dmUsers:
        await bot.get_user(user).send(message)

async def watchMayor():
    while True:
        mayorData = hypixleimpl.getMayorData()
        for i in range(len(mayorData["current"])):
            if mayorData["current"][i]["name"] == "Diana":
                await dmUsers(f"Diana is the mayor!")
                break
        else:
            print("diana is not mayor")
        
        await asyncio.sleep(46400)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    #asyncio.run(watchMayor())
    bot.run(discToken)