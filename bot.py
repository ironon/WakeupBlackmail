from awake import heIsNotAwakeButHeShouldBe
import awake
import discord
import json
from typing import Callable
import atexit
import asyncio
from discord.ext import commands, tasks
# pylint: disable=assigning-non-slot
intents = discord.Intents.default()
intents.message_content = True
callbackFunc = None
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
try:
    blackmailChannel = open("channel.txt", "r").read()
except:
    blackmailChannel = open("channel.txt", "w+").read()
print("Blackmail Channel: " + blackmailChannel)
async def send(m:str, view=None):
    if blackmailChannel != "":
        channel = await client.fetch_channel(blackmailChannel)
        await channel.send(m, view=view)
       
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(blackmailChannel)
    await send("I am ready.")
    checkIfAwake.start()


@tree.command(name="setblackmailchannel", description="set where slumbertime blabbers", guild=discord.Object(id=663008643763142678))
async def set_channel(interaction: discord.Interaction):
    global blackmailChannel
    blackmailChannel = interaction.channel.id
    await interaction.response.send_message("ok nerd", ephemeral=True)

@tasks.loop(seconds=3)
async def checkIfAwake():
    if await check():
        checkIfAwake.stop()
        await inSync()
        
async def sendBlackmailNotification():
    view = Claim()
    await send("DAVID SLEPT IN TOO MUCH ☠️", view=view)

async def check():
    if heIsNotAwakeButHeShouldBe():
        awake.heWokeUpLate()

        await sendBlackmailNotification()
        return True
    return False

async def inSync():
    await asyncio.sleep(86300)
    checkIfAwake.start()
            
def setWakeupCallback(func:Callable):
    global callbackFunc
    callbackFunc = func

            
class Claim(discord.ui.View):
    @discord.ui.button(label="GET DAVID TICKET", style=discord.ButtonStyle.green)
    async def sendDM(self, interaction: discord.Interaction, button: discord.ui.button):
        link = callbackFunc()
        await interaction.user.send("claim here: \n" + link)
        await interaction.response.send_message("check ur dms", ephemeral=True)



def exit_handler():
    f = open("channel.txt", "w+")
    f.write(str(blackmailChannel))
    f.close()
atexit.register(exit_handler)

def main():
      # client.loop.create_task(checkIfAwake(c))
   
    token = json.load(open("secret.json", "r"))['discord']
    client.run(token=token)

if __name__ == '__main__':
    main()


