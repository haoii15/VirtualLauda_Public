import pandas as pd
COLOR = "#36393e"
FONT = "Sans-serif"

def styleDf(df):

    styled = df.style.set_table_styles(
    [{'selector': 'th',
    'props': [('background', COLOR), 
                ('color', 'white'),
                ('font-family', FONT)]},
    
    {'selector': 'td',
    'props': [('font-family', FONT),
                ('color', 'white')]},

    {'selector': 'tr:nth-of-type(odd)',
    'props': [('background', COLOR)]}, 
    
    {'selector': 'tr:nth-of-type(even)',
    'props': [('background', COLOR)]},
    
    ]
    )

    return styled.format(precision=3)

def listToDf(list):
    df = pd.DataFrame(list, columns = ["rank", "navn", "level", "xp", "meldingar"])
    return styleDf(df)

def llistToDf(list, columns):
    df = pd.DataFrame(list, columns = columns)
    df.index += 1
    return styleDf(df)