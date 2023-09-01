import discord
import dataframe_image as dfi
from disc.http_client import http_client
from secret import g_url,adminid
from services.df import llistToDf



async def flip(client, message):
    if message.author.id == adminid:
        msg = message.content.split(" ", 1)
        if len(msg) < 2:
            await message.channel.send("Format: !link <grand prix")
            return
        gp_name = msg[1]

        resp = http_client.put(g_url+f"{gp_name}").json()
        await message.channel.send(resp["detail"])
    else:
        await message.channel.send("kun admin")

async def gps(client, message):
    request = http_client.get(g_url).json()
    if request["code"] != 200:
        await message.channel.send(request["detail"])
        return
    
    toprow = ["Name", "Season", "Track", "Condition", "Game", "Held"]
    df = llistToDf(request["detail"], toprow)
    dfi.export(df, "imgs/gps.png")

    await message.channel.send(file=discord.File("imgs/gps.png"))