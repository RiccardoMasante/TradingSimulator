''' 
ESEMPIO
Esempio semplice che esengue una callback per stampare la candela appena conclusa sul TF a 1 minuto.
'''


import os,sys
current_path = os.getcwd() 
sys.path.insert(0,current_path + r"/../pybit")  

from pybit.unified_trading import WebSocket
from time import sleep
import time
from pybit.unified_trading import HTTP


ws = WebSocket(
    testnet=True,
    channel_type="linear",
)
session = HTTP(testnet=True)

def new_candle(message):
    print(message)
    print(time.time())
    candles= session.get_kline(
    category="inverse",
    symbol="BTCUSD",
    interval=1,
    limit=5
    )
    print(candles)
    
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