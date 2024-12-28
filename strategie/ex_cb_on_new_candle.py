import os,sys
current_path = os.getcwd() 
sys.path.insert(0,current_path + r"/../pybit")  

from pybit.unified_trading import WebSocket
from time import sleep
import time

ws = WebSocket(
    testnet=True,
    channel_type="linear",
)

def new_candle(message):
    print(message)
    print(time.time())
    
def handle_message(message):
    if message["data"][0]["confirm"]:
        new_candle(message)


#interval defined in minutes
ws.kline_stream(
    interval=1,
    symbol="BTCUSDT",
    callback=handle_message
)
while True:
    sleep(1)