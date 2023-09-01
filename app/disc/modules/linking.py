import os
import pickle as pkl
from disc.http_client import http_client
from secret import u_url, verifications, pending_path


async def link(client, message):
    msg = message.content.split(" ", 1)
    if len(msg) < 2:
        await message.channel.send("Format: !link <førernavn>")
        return

    request = http_client.get(u_url+"link/verify/"+msg[1]+f"?discord_id={message.author.id}").json()
    if request["code"] != 200:
        if request["error"] == 2:
            resp, disc_id = request["detail"].split(":", 1)
            resp += ": " + client.get_user(int(disc_id)).mention
            await message.channel.send(resp)
        else:
            await message.channel.send(request["detail"].strip('"'))
        return

    if os.path.getsize(pending_path) > 0:
        with open(pending_path, "rb") as file:
            pending = pkl.load(file)
    else:
        pending = [0]

    if message.author.id in pending:
        await message.channel.send("Du har allerede en linkforespørsel som ligge å vente på godkjenning.")
        return
    else:
        pending.append(message.author.id)
        with open(pending_path, "wb") as file:
            pkl.dump(pending, file)

    new_msg = f'''{msg[1]}, {message.author.name}, {message.author.id}'''
    await client.get_channel(verifications).send(new_msg)
    await message.channel.send("Linkforespørselen din e sendt te verifisering, eg gjer lyd når den e good")


async def unlink(client, message):
    request = http_client.put(u_url+"unlink"+f"?discord_id={message.author.id}").json()
    if request["code"] == 200:
        await message.channel.send(message.author.mention + "e isje lenger linka te " + request["detail"])
    else:
        await message.channel.send(request["detail"])


async def rename(client, message):
    names = message.content.split(" ", 1)
    if len(names) < 2:
        await message.channel.send("Feil format; !rn <driver name>:<new name>")
        return
    try:
        driver_name, new_name = message.channel.split(":", 1)
        request = http_client.patch(u_url+f"name/{driver_name}/{new_name}").json()
        await message.channel.send(request["detail"])
    except:
        await message.channel.send("Feil format; !rn <driver name>:<new name>")
        return
        