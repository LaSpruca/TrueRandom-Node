import websocket
import threading
import os
import time
import random
from roll_alg import roll_read_dice_procedure

from dotenv import load_dotenv
load_dotenv()


# Get the environment variables
env = os.environ

# Get secrete key
key = env.get("SECRETE_KEY")
if key == None:
    key = ""


queue = []

def on_message(ws, message):
    global queue
    print("received message",message)
    if message == "ping":
        ws.send("pong")
    else:
        queue.append(message)


def on_error(ws, error):
    print(error)
    ws.close()


def on_close(ws):
    print("[WEBSOCKET] Closed, Reconnecting")
    ws.close()


def on_open(ws):
    global handle_thread
    print("Websocket Opened")
    def run(*args):
        ws.send(key)
    threading.Thread(target=run, args=()).start()

def clear():
    global ws
    global queue
    ws.close()
    queue = []    


def roll_queue():
    global ws
    global queue
    while True:
        try:
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
                        ws.send("!" + str(result))

                else:  # A single roll
                    print(f"[ROLLER] Handeling UUID request: {request}")
                    result = roll_read_dice_procedure()
                    value = request + "|" + str(result)
                    ws.send(value)

                del queue[0]
        except Exception as e:
            print("Roll Queue failed",e)
            pass
        time.sleep(0.1)

def connect_to_websocket():
    global ws
    print("Generating websocket app")
    ws = websocket.WebSocketApp("ws://tr.host.qrl.nz/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    print("Opening")

    ws.on_open = on_open
    ws.run_forever()
if __name__ == "__main__":
    global roll_queue_handle

    roll_queue_handle = threading.Thread(target=roll_queue)
    roll_queue_handle.start()
    while True:
        connect_to_websocket()
        try:
            ws.close()
        except Exception:
            # imagine
            pass
    
