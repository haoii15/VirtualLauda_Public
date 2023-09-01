

async def help(client, message):
    msg = message.content.split(" ", 1)
    if len(msg) == 1:
        m = '''Du trenge hjelp ja, men te ka?\n-"!help teams" for alt angåande lag\n-"!help drivers" for alt om linking mellom discord og førere osv\n-"!help ranks" for koss å henta diverse tabellar'''
        await message.channel.send(m)
        return

    else:
        buzz = msg[1]

        if buzz == "teams":
            m = '''Følgane commands finns for teams:\n-"!teams" gir deg ei lista av alle lag\n-"!create <lagnavn>" ganske greit, lage et lag\n-"!join <lagnavn>" sende ein forespørsel om å få ver me på et allerede eksiterane lag\n-"!leave" sjølforklarane, forlate de lage du e på atm\n-"!transfer <lagnavn:ny eiar>" du gjer fra deg eiarrollen i lage te ein aen\n-"!remove <førernavn>" du fjerne ein fører fra et lag du e eiar av'''
            await message.channel.send(m)
        elif buzz == "drivers":
            m = '''Følgane commands finns for linking og førerlogistikk:\n-"!drivers" gir ei lista av alle førere\n-"!link <førernavn>" linke discord til førerkonto, bruk !drivers på forhånd for å være sikker på at du bruker rett navn. Dersom navne ikke finnes fra før lages en ny bruker.\n"!unlink" unlink gjeldene link'''
            await message.channel.send(m)
        elif buzz == "ranks":
            m = '''Følgane commands finns for stats og tabeller:\n-"!total" gjer total scoreboard for alle løp fra alle sesongar\n-"!total <sesong>" gjer scoreboard for ein spesifikke sesong\n-"!gp <Grand Prix-navn>" gjer scoreboard fra et spesifikt Grand Prix\n-"!gp <Grand Prix-navn>:<førernavn>" gjer alle rundane te ein førar for gitte Grand Prix\n-"!gpall" gjer ei lista øve alle Grand Prix\n\nHer komme de ein del mer, trengs ein command for å hente Grand Prix liste, pluss diverse for å skilla ud sesonger og hubs fra total. Fort gjort, komme om isje for lenge.'''
            await message.channel.send(m)
        else:
            await message.channel.send("De der kan eg sje hjelpa deg me på nåverande tidspunkt")