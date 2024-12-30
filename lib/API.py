import os,sys
sys.path.insert(0,os.getcwd()  + r"/../pybit")  

from pybit.unified_trading import HTTP
sys.path.insert(0,os.getcwd()  + r"/..")  
import chiavi

from datetime import datetime

class API():
    def __init__(self,exchange):
        #TODO download the number of candles
        self.limit_number_candles = 1000

        self.exchange = exchange

        self.debug = int(os.environ["DEBUG"])

        if exchange=="bybit":
            self.session = HTTP(
                #testnet=True,
                api_key=chiavi.api_key,
                api_secret=chiavi.api_secret
            )


    def get_currency(self,symbol):
        if self.exchange =="bybit":
            
            # get the coin of the simbol
            info = self.session.get_instruments_info(
                category="linear",
                symbol=symbol,
                )
            return info["result"]["list"][0]["baseCoin"]
            pass

    def download_n_candles(self,symbol,time_frame,stop_time):
        if self.exchange =="bybit":
            candles_reformatted = {}

            candles= self.session.get_kline(
                category="linear",
                symbol=symbol,
                interval=time_frame,
                end = stop_time,
                limit = self.limit_number_candles
            )
            #example of output
            #{'retCode': 0, 'retMsg': 'OK', 'result': {'symbol': 'BTCUSDT', 'category': 'inverse', 'list': [['1735563300000', '94018.3', '94018.3', '93332.1', '94018.3', '10.325', '967952.4412'], ['1735563240000', '94018.3', '94018.3', '93332.1', '94018.3', '13.408', '1255364.7031'], ['1735563180000', '94018.3', '94018.3', '93332.1', '94018.3', '9.959', '933537.047'], ['1735563120000', '93737.9', '94018.3', '93332.1', '94018.3', '10.577', '991447.7261'], ['1735563060000', '94018.3', '94018.3', '93332.1', '93737.9', '7.268', '680399.6031'], ['1735563000000', '92936', '94018.3', '92936', '94018.3', '13.781', '1291594.0053'], ['1735562940000', '93288.8', '93332.1', '92936', '92936', '14.466', '1350110.5612'], ['1735562880000', '92558.9', '93288.8', '92558.9', '93288.8', '9.988', '926228.7949'], ['1735562820000', '92936', '93332.1', '92558.9', '92558.9', '17.546', '1627090.0607'], ['1735562760000', '92607.3', '93332.1', '92558.9', '92936', '13.53', '1256593.3229']]}, 'retExtInfo': {}, 'time': 1735563359619}
            i = self.limit_number_candles-1
            for candle in candles["result"]["list"]:
                candles_reformatted[i] = {}
                candles_reformatted[i]["t"] = int(candle[0])
                candles_reformatted[i]["t_s"] = datetime.utcfromtimestamp(int(candle[0])/1000).strftime("%Y-%m-%d %H:%M:%S")
                candles_reformatted[i]["o"] = float(candle[1])
                candles_reformatted[i]["h"] = float(candle[2])
                candles_reformatted[i]["l"] = float(candle[3])
                candles_reformatted[i]["c"] = float(candle[4])
                candles_reformatted[i]["v"] = float(candle[5])
                i = i - 1

            return candles_reformatted


