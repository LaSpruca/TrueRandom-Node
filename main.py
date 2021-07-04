import websocket
import threading
import os
import time
from dotenv import load_dotenv
import random
from roll_alg import roll_read_dice_procedure

twitch_enabled = True


load_dotenv()

# Get the environment variables
env = os.environ

# Get secrete key
key = env.get("SECRETE_KEY")
if key == None:
    key = ""


if twitch_enabled:
    from twitch import initialize_twitch
    threading.Thread(target=initialize_twitch, args=()).start()

from roll_alg import roll_dice

queue = []


def on_message(ws, message):
    print(f"[MESSAGE HANDLER] Received message {message}")
    queue.append(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("[WEBSOCKET] Closed")


def on_open(ws):
    print("Websocket Opened")
    def run(*args):
        ws.send(key)
    threading.Thread(target=run, args=()).start()
    threading.Thread(target=handle, args=(ws,)).start()


def handle(websocket):
    while True:
        if len(queue) > 0:
            request = queue[0]
            print(f"[ROLLER] Handling {request}")
            if request.startswith("!"):  # Processing a buffer
                print(
                    f"[ROLLER] Handling batch with {int(request[1:])} rolls")
                # Roll as many times as the API requires
                for i in range(0, int(request[1:])):
                    result = roll_read_dice_procedure()

                    # Send to websocket
                    websocket.send("!" + str(result))

            else:  # A single roll
                print(f"[ROLLER] Handeling UUID request: {request}")
                result = roll_read_dice_procedure()
                value = request + "|" + str(result)
                websocket.send(value)

            del queue[0]




if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://tr.host.qrl.nz/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
