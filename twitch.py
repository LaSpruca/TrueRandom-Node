import os
from twitchio import *
from twitchio.ext import commands

from roll_alg import roll_read_dice_procedure

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.environ['TWITCH_ACCESS_TOKEN'],  prefix='!',
                         initial_channels=['TrueRandomQRL'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | tes')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='roll')
    async def roll_command(self, ctx):
        result = roll_read_dice_procedure()
        await ctx.send(f'Hello {ctx.author.name}!')


def initialize_twitch():
    global bot
    # print("test")
    # bot = commands.Bot(
    #     # set up the bot
    #     irc_token=os.environ['TWITCH_TMI_TOKEN'],
    #     client_id=os.environ['TWITCH_CLIENT_ID'],
    #     nick="True Random",
    #     prefix="BOT",
    #     initial_channels="truerandomqrl"
    # )

    # bot.run()

    # @bot.event
    # async def event_ready():
    #     'Called once when the bot goes online.'
    #     print(f"{os.environ['BOT_NICK']} is online!")
    #     ws = bot._ws  # this is only needed to send messages within event_ready
    #     await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")
    bot = Bot()
    bot.run()

if __name__=="__main__":
    from dotenv import load_dotenv
    # import dice_content


    load_dotenv()
    initialize_twitch()