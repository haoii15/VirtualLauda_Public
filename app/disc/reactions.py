import os
import pickle as pkl
from secret import adminid, verifications, verify, deny, u_url, pending_path, shitchat, team_pending_path, t_url
from disc.http_client import http_client


async def reaction_handler(client, reaction, user):
    if user.id == adminid and reaction.message.channel.id == verifications:
        msg_s = reaction.message.content.strip('"').split(", ")
        if reaction.emoji.id == verify:
            if len(msg_s) != 3:
                await reaction.message.channel.send("Fiks de her, denne sko vert len 3 på split , ^^^")
                return
            request = http_client.put(u_url+"link/"+msg_s[0]+f"?discord_id={msg_s[2]}")
            await client.get_channel(shitchat).send(client.get_user(int(msg_s[2])).mention + " e nå linka te " +request.json()["detail"])
            with open(pending_path, "rb") as file:
                pending = pkl.load(file)
            pending.remove(int(msg_s[2]))
            if len(pending) > 0:
                with open(pending_path, "wb") as file:
                    pkl.dump(pending, file)

            await reaction.message.delete()

        elif reaction.emoji.id == deny:
            with open(pending_path, "rb") as file:
                pending = pkl.load(file)
            pending.remove(int(msg_s[2]))
            if len(pending) > 0:
                with open(pending_path, "wb") as file:
                    pkl.dump(pending, file)

            await client.get_channel(shitchat).send(client.get_user(int(msg_s[2])).mention + " , link requesten din e avslått")
            await reaction.message.delete()

    if reaction.message.channel.id == shitchat:
        if os.path.getsize(team_pending_path) > 0:
            with open(team_pending_path, "rb") as file:
                pending = pkl.load(file)
        else:
            pending = [{"owner": "None", "joiner": 0, "message_id": 0}]
        tmp = None
        for req in pending:
            if req["message_id"] == reaction.message.id:
                tmp = req   
                break 

        if tmp == None:
            return
        
        if tmp["owner"] != str(user.id):
            return
        
        if reaction.emoji.id == verify:
            joiner = tmp["joiner"]
            team_name = reaction.message.content.split(" ", 1)[1]
            resp = http_client.put(t_url + "join/" + team_name + f"?discord_id={joiner}").json()
            if resp["code"] == 200:
                seed = resp["detail"]
            else:
                await reaction.message.channel.send(resp["detail"])
                return
            await reaction.message.channel.send(f"{client.get_user(joiner).mention} har nå joina {team_name} og laget har fått seednivå {seed}")
            await reaction.message.delete()
            pending.remove(tmp)
            with open(team_pending_path, "wb") as file:
                pkl.dump(pending, file)
        
        elif reaction.emoji.id == deny:  
            owner, joiner  = tmp["owner"], tmp["joiner"]
            await reaction.message.channel.send(f"{client.get_user(joiner).mention}, {client.get_user(owner).mention} har avslått forespørselen din om å joine {team_name}")
            await reaction.message.delete()
            pending.remove(tmp)
            with open(team_pending_path, "wb") as file:
                pkl.dump(pending, file)
