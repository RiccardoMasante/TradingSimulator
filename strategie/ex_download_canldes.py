''' 
ESEMPIO
Esempio semplice che scarica le ultime 200 candele sul TF a 1 minuto.
'''

import os,sys
current_path = os.getcwd() 
sys.path.insert(0,current_path + r"/../pybit")  

from pybit.unified_trading import HTTP
session = HTTP(testnet=True)
candles= session.get_kline(
    category="inverse",
    symbol="BTCUSD",
    interval=1
)
print(candles)
print(len(candles["result"]["list"]) )