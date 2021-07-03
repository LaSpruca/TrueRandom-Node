import os
from twitchio import *
from twitchio.ext import commands


def initialize_twitch():
    global bot
    print("test")
    bot = commands.Bot(
        # set up the bot
        irc_token=os.environ['TWITCH_TMI_TOKEN'],
        client_id=os.environ['TWITCH_CLIENT_ID'],
        nick="True Random",
        prefix="BOT",
        initial_channels="truerandomqrl"
    )

    bot.run()
    
    @bot.event
    async def event_ready():
        'Called once when the bot goes online.'
        print(f"{os.environ['BOT_NICK']} is online!")
        ws = bot._ws  # this is only needed to send messages within event_ready
        await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")