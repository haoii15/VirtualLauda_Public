import discord, os
from disc.commands import cmd_handler
from disc.reactions import reaction_handler
from secret import shitchat, controller

intents = discord.Intents.default()
intents.members = True
# intents.message_content = True
client = discord.Client(intents=intents)

channels = [shitchat, controller]

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    msg = message.content

    if msg.startswith("!"):
        if message.channel.id in channels:
            await cmd_handler(client, message)
        else:
            await message.channel.send(f"Du kan kun snakka me Lauda i {client.get_channel(shitchat).mention}")

@client.event
async def on_reaction_add(reaction, user):
    await reaction_handler(client, reaction, user)

client.run()