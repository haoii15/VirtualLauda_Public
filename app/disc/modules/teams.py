import discord
import os
import pickle as pkl
import dataframe_image as dfi
from disc.http_client import http_client
from secret import t_url, u_url, team_pending_path, klubbhus, shitchat, deny, verify
from services.df import llistToDf

# test

async def create_team(client, message):
    '''who ever, the creator is set as first driver and owner'''
    msg = message.content.split(" ", 1)
    if len(msg) < 2:
        await message.channel.send("Format: !create <lagnavn>")
        return
    team_name = msg[1]
    request = http_client.post(t_url + team_name + f'''?discord_id={message.author.id}''').json()
    if request["code"] != 200:
        await message.channel.send(request["detail"])
        return

    await message.channel.send(f"Du har nå gjort deg sjøl te eigar av de nya lage **{team_name.upper()}**")

async def join_team(client, message):
    '''who ever who is not already in a team. First have to leave team'''
    msg = message.content.split(" ", 1)
    if len(msg) < 2:
        await message.channel.send("Format: !join <lagnavn>")
        return
    team_name = msg[1]
    resp = http_client.get(u_url + f"discord/{message.author.id}").json()
    if resp["code"] == 400:
        await message.channel.send(resp["detail"])
        return
    driver = resp["detail"]
    if driver["team"] != None:
        await message.channel.send(f'''Du har allerede kontrakt med {http_client.get(t_url + "id/" + driver["team"]).json()["detail"]["name"]}''')
        return
    resp = http_client.get(t_url + team_name).json()
    if resp["code"] == 400:
        await message.channel.send(resp["detail"])
        return
    team = resp["detail"]

    if os.path.getsize(team_pending_path) > 0:
        with open(team_pending_path, "rb") as file:
            pending = pkl.load(file)
    else:
        pending = [{"owner": "None", "joiner": 0, "message_id": 0}]

    for pen in pending:
        if message.author.id == pen["joiner"]:
            await message.channel.send("Du har allerede en linkforespørsel som ligge å vente på godkjenning.")
            return
    

    owner = http_client.get(u_url+f'''id/{team["owner"]}''').json()
    if owner == None:
        await message.channel.send(owner["detail"])
        return
    owner = owner["detail"]
    pending.append({"owner": owner["discord_id"], "joiner": message.author.id, "message_id": message.id})
    owner = client.get_user(int(owner["discord_id"]))
    if owner == None:
        await message.channel.send("eiar av laget e isje kobla te e førerkonto")
        return
    
    with open(team_pending_path, "wb") as file:
        pkl.dump(pending, file)
    
    new_msg = f'''Du har en ny fører som ønske å joine lage ditt {team["name"]}. Reager på {message.jump_url} med en {f"<:check:{verify}>"} for å godta forespørselen eller en {f"<:cringe:{deny}>"} for å avslå den.'''
    channel = owner.dm_channel
    if channel == None:
        channel = await owner.create_dm()
    await channel.send(new_msg)
    await message.channel.send("Forespørselen e lagt te godkjenning. Når den e besvart komme eg tebake te deg.") 

async def teams(client, message):
    msg_ = message.content.split(" ", 1)
    if len(msg_)== 1:
        resp = http_client.get(t_url).json()
        if resp["code"] == 200:
            df = llistToDf(resp["detail"], ["name", "1. driver", "2. driver", "seed", "created", "created by", "owner"])

            dfi.export(df, "imgs/teams.png")
    
            await message.channel.send(file=discord.File("imgs/teams.png"))
        else:
            await message.channel.send("ingen lag å hente")
    else:
        await message.channel.send("not implemented")


async def leave_team(client, message):
    '''who ever, if owner leaves, the second driver is promoted to owner'''
    '''if the last person leaves, deletes the team'''
    request = http_client.put(t_url + "leave/" + str(message.author.id)).json()
    await message.channel.send(request["detail"])

async def transfer_team(client, message):
    '''owner only'''
    data = message.content.split(" ", 1)
    if len(data) < 2: 
        await message.channel.send("feil format! !transfer <lag navn>:<ny eiar>")
        return
        
    data = data[1]
    navn = data.split(":")
    if len(navn) != 2:
        await message.channel.send("feil format! !transfer <lag navn>:<ny eiar>")
        return

    team_name, owner_name = navn
    request = http_client.put(t_url + f"owner?team_name={team_name}&owner_id={message.author.id}&new_owner_name={owner_name}").json()
    await message.channel.send(request["detail"])

async def remove_driver(client, message):
    '''owner only'''
    data = message.content.split(" ", 1)
    if len(data) < 2:
        await message.channel.send("feil format! !remove <fører navn>")
        return
        
    driver_name = data[1]
    request = http_client.put(t_url + f"remove?driver_name={driver_name}&owner_id={message.author.id}").json()
    await message.channel.send(request["detail"])