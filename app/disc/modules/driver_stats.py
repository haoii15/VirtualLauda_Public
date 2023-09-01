import discord
import dataframe_image as dfi
from disc.http_client import http_client
from secret import u_url
from services.df import llistToDf



async def fetch_drivers(client, message):
    request = http_client.get(u_url).json()
    if request["code"] == 400:
        await message.channel.send(request["detail"])
        return
    
    l = []
    for driver in request["detail"]:
        disc = client.get_user(int(driver["discord_id"])).name if driver["discord_id"] else None
        l.append([driver["name"], driver["display_name"], driver["team"], disc])
    toprow = ["Name", "Display Name", "Team", "Discord"]
    df = llistToDf(l, toprow)
    dfi.export(df, "imgs/drivers.png")

    await message.channel.send(file=discord.File("imgs/drivers.png"))




