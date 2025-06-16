import discord
from discord.ext import commands
import hypixleimpl
import asyncio
import json, atexit

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
dianaEmbed = discord.Embed(title="Diana is running!", description="Diana is running with the Mythological Ritual perk!", color=discord.Color.gold())

def loadConfig():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config['discToken'], config['guildId']
    except FileNotFoundError:
        print("config.json not found")
        with open("config.json", "w") as f:
            json.dump({"discToken": "", "guildId": ""}, f, indent=4)
        print("config.json created with defaults")
        return None, None
    except KeyError as e:
        print(f"config.json missing required fields: {e}")
        return None, None

discToken, guildId = loadConfig()

notifList = []
# load notif list
try:
    with open("notifList.json", "r") as f:
        notifList = json.load(f)
except FileNotFoundError:
    print("notifList.json not found")

# enrolls user to receive notifications
@bot.slash_command(name="getnotifs", guild_ids=[guildId])
async def getnotifs(interaction):
    # check if user is in the userlist
    if interaction.author.id not in notifList:
        await interaction.respond("You have been added to the list of users to receive notifications.", ephemeral=True, delete_after=10)
        notifList.append(interaction.author.id)
    else:
        await interaction.respond("You are already on the list of users to receive notifications.", ephemeral=True, delete_after=10)

# gets the current mayor
@bot.slash_command(name="mayor", guild_ids=[guildId])
async def mayor(interaction):
    mayorData = hypixleimpl.getMayorData()

    embed = discord.Embed(title="Current Mayor", 
                          description=f"The current mayor is {mayorData['mayor']['name']}")
    
    await interaction.respond(embed=embed, ephemeral=True)

# temp command to save data
#@bot.slash_command(name="savedata", guild_ids=[guildId])
async def saveData(interaction):
    electionData = hypixleimpl.getMayorData()
    with open("electionData.json", "w") as f:
        json.dump(electionData, f, indent=4)


# checks if any mayor is running that would have the mythological ritual perk
@bot.slash_command(name="checkevent", guild_ids=[guildId])
async def checkevent(interaction):
    electionData = hypixleimpl.getMayorData()
    candidates = electionData["current"]["candidates"]
    for i in range(len(candidates)):
        if candidates[i]["name"] == "Jerry":
            embed = discord.Embed(title="Jerry is running for mayor!", description="Jerry is running for mayor", color=discord.Color.gold())
            await interaction.respond(embed=dianaEmbed, ephemeral=True)

        if candidates[i]["name"] == "Diana":
            perks = candidates[i]["perks"]

            for j in range(len(perks)):

                if perks[j]["name"] == "Mythological Ritual":
                    await interaction.respond(embed=dianaEmbed, ephemeral=True)
                    break
        
# sends a message to all users in the dmUsers list
async def dmUsers(message=None, embed=None):
    for user in notifList:
        if embed is None:
            await bot.get_user(user).send(message)
        else:
            await bot.get_user(user).send(embed=embed)

async def watchMayor():
    while True:
        mayorData = hypixleimpl.getMayorData()
        for i in range(len(mayorData["current"])):
            if mayorData["current"][i]["name"] == "Diana":
                await dmUsers(embed=dianaEmbed)
                break
        else:
            print("diana is not mayor")
        
        # check every 5 hours
        await asyncio.sleep(3600 * 12)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def exitHandler():
    with open("notifList.json", "w") as f:
        json.dump(notifList, f, indent=4)
    print("Notif list saved")


atexit.register(exitHandler)


async def main():
    print("Bot is ready")
    await bot.start(discToken)
    asyncio.create_task(watchMayor())

if __name__ == "__main__":
    asyncio.run(main())
