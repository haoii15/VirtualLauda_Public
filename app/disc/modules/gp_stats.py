import dataframe_image as dfi
import discord
from disc.http_client import http_client
from services.df import llistToDf
from secret import s_url, g_url


async def total(client, message):
    msg = message.content.split(" ", 1)
    if len(msg) == 1:
        request = http_client.get(s_url).json()  
        toprow = ["Name", "Team", "Points"]
        df = llistToDf(request, toprow)

        dfi.export(df, "imgs/total.png")
        
        await message.channel.send(file=discord.File("imgs/total.png"))
    else:
        msg, season = msg
        seasons = http_client.get(g_url + "seasons/all").json()
        if seasons["code"] != 200:
            await message.channel.send(seasons["detail"])
            return
        seasons = seasons["detail"]
        try:
            season = int(season)
        except:
            await message.channel.send(f"{season} e isje et tal")
            return
        if season in seasons:
            request = http_client.get(s_url + f"season/{season}").json()
            toprow = ["Name", "Team", "Points"]
            df = llistToDf(request, toprow)

            dfi.export(df, f"imgs/total{season}.png")

            await message.channel.send(file=discord.File(f"imgs/total{season}.png"))
        else:
            await message.channel.send(f"{season} e isje ein sesong")


async def gp(client, message):
    msg = message.content.split(" ", 1)
    if msg[1].count(":"):
        gp_name, driver_name = msg[1].split(":", 1)
        request = http_client.get(g_url+f"laps/{driver_name}/{gp_name}").json()
        if request["code"] != 200:
            await message.channel.send(request["detail"])
            return
        toprow = ["Name", "Sector 1", "Sector 2", "Sector 3", "Lap Time", "Valid", "Hub"]
        df = llistToDf(request["detail"], toprow)
        dfi.export(df, f"imgs/{driver_name}_{gp_name}.png")
        
        await message.channel.send(file=discord.File(f"imgs/{driver_name}_{gp_name}.png"))

    else:
        request = http_client.get(s_url+"gp/"+msg[1]).json()
        if isinstance(request, str):
            await message.channel.send(request)
            return
        if request:
            toprow = ["Name", "Sector 1", "Sector 2", "Sector 3", "Lap Time", "Team", "Points"]
            df = llistToDf(request, toprow)

            dfi.export(df, f"imgs/{msg[1]}.png")

            await message.channel.send(file=discord.File(f"imgs/{msg[1]}.png"))
        else:
            await message.channel.send(f"{msg[1]} e isje någe Grand Prix")


async def driver(client, message):
    pass