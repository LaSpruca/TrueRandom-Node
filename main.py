import asyncio
import websockets
import os
from dotenv import load_dotenv


async def main():
    # Load the .env file
    load_dotenv()

    # Get the environment variables
    env = os.environ

    # Get secrete key
    key = env.get("SECRETE_KEY")
    if key == None:
        key = ""

    # The URL of the webserver
    uri = "ws://tr.host.qrl.nz:3456/"

    # Connect to the websocket
    async with websockets.connect(uri) as websocket:
        # Authenticate with the API
        websocket.send(key)

        queue = []

        # Forward any requests to be handled synchronously
        async for request in websocket:
            queue.put(request)

        while True:
            if len(queue) > 0:
                with queue[0] as request:
                    if request.starts_with("!"):  # Processing a buffer
                        # Roll as many times as the API requires
                        for i in range(0, int(request[1:])):
                            # TODO: Roll
                            result = 5
                            # Send to websocket
                            websocket.send("!" + result)

                    else:  # A single roll
                        # TODO: Roll
                        result = 5
                        value = request + "|" + result
                        websocket.sens(value)

                    del queue[0]


asyncio.get_event_loop().run_until_complete(main())
