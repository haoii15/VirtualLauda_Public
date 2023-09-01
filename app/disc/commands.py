from .modules.gp_stats import total, gp
from .modules.linking import link, unlink, rename
from .modules.teams import create_team, join_team, leave_team, teams, transfer_team, remove_driver
from .modules.gp import flip, gps
from .modules.driver_stats import fetch_drivers
from .modules.help import help
from .modules.query import query


async def cmd_handler(client, message):
    cmd = message.content.split(" ")[0]

    if message.content.count(";") > 0:
        await message.channel.send("fuck deg")
        return

    if cmd in commands.keys():
        await commands[cmd](client, message)

commands = {
    "!total": total,
    "!gp" : gp,
    "!link": link,
    "!unlink": unlink,
    "!create" : create_team,
    "!join" : join_team,
    "!teams" : teams,
    "!transfer" : transfer_team,
    "!remove" : remove_driver,
    "!leave" : leave_team,
    "!flip" : flip,
    "!drivers": fetch_drivers,
    "!help": help,
    "!gpall": gps,
    "!rn": rename,
    "!query": query
}