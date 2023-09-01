from disc.http_client import http_client
from secret import a_url






async def query(client, message):
    q = message.content.split(" ", 1)[1]

    if len(q) < 2:
        await message.channel.send("Feil format; !query <query>")
        return
    
    request = http_client.put(a_url + "query", json=q).json()
    await message.channel.send(request["detail"])
