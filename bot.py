from isAwake import isAwake
import discord
import json
import atexit
from discord.ext import commands
# pylint: disable=assigning-non-slot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
try:
    blackmailChannel = open("channel.txt", "r").read()
except:
    blackmailChannel = open("channel.txt", "w+").read()
print("Blackmail Channel: " + blackmailChannel)
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(blackmailChannel)
    if blackmailChannel != "":
        channel = await client.fetch_channel(blackmailChannel)
        await channel.send("I am ready.")


@tree.command(name="setblackmailchannel", description="set where slumbertime blabbers", guild=discord.Object(id=663008643763142678))
async def set_channel(interaction: discord.Interaction):
    global blackmailChannel
    blackmailChannel = interaction.channel.id
    await interaction.response.send_message("ok nerd", ephemeral=True)

def exit_handler():
    f = open("channel.txt", "w+")
    f.write(str(blackmailChannel))
    f.close()
atexit.register(exit_handler)

def main():
    token = json.load(open("secret.json", "r"))['discord']
    client.run(token=token)

if __name__ == '__main__':
    main()


