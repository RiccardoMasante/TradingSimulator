import os,sys
sys.path.insert(0,os.getcwd()  + r"/../pybit")  
from pybit.unified_trading import HTTP
sys.path.insert(0,os.getcwd()  + r"/..")  
import chiavi

session = HTTP(
    #testnet=True,
    api_key=chiavi.api_key,
    api_secret=chiavi.api_secret
)
price = 10000
print(session.place_order(
    category="linear",
    symbol="BTCUSDT",
    side="Buy",
    orderType="Limit",
    qty="0.001",
    price=str(price),
    timeInForce="PostOnly",
    #orderLinkId="spot-test-postonly2",
    isLeverage=0,
    orderFilter="Order",
    takeProfit = str(price+5),
    stopLoss = str(price-10000),
    tpslMode = "Partial",
    tpLimitPrice = str(price+10),
    #slLimitPrice
    tpOrderType = "Limit",
    #slOrderType = "Market"
))