import os,sys
current_path = os.getcwd() 
sys.path.insert(0,current_path + r"/../pybit")  
from pybit.unified_trading import HTTP
sys.path.insert(0,current_path + r"/..")  
import chiavi

session = HTTP(
    #testnet=True,
    api_key=chiavi.api_key,
    api_secret=chiavi.api_secret
)
print(session.place_order(
    category="linear",
    symbol="BTCUSDT",
    side="Buy",
    orderType="Limit",
    qty="0.001",
    price="15000",
    timeInForce="PostOnly",
    orderLinkId="spot-test-postonly1",
    isLeverage=0,
    orderFilter="Order",
    #takeProfit = "90000",
    #stopLoss = "90000",
    #tpslMode = "Partial",
    #tpLimitPrice = "94650",
    #slLimitPrice
    #tpOrderType = "Limit",
    #slOrderType = "Market"
))