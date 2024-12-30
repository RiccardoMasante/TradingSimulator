
from log import log
import API
import os
import json
import datetime

class Simulator():
    def __init__(self,time_inizio,time_fine,time_frame,a_mercato,symbol,starting_index,portafoglio,exchange="bybit",factor_limit_tax = 0.9998,factor_market_tax = 0.9995,name="no_name"):
        self.debug = int(os.environ["DEBUG"])
        self.name = name

        self.factor_limit_tax = factor_limit_tax
        self.factor_market_tax = factor_market_tax

        self.time_inizio_int = int(time_inizio.timestamp()*1000)
        self.time_fine_int = int(time_fine.timestamp()*1000)
        if self.debug >0:
            log(str(self.time_inizio_int))
            log(str(self.time_fine_int))
        self.time_frame = time_frame
        self.time_frame_min = self.translate_time_frame_in_min(time_frame)
        self.time_frame_ms = self.time_frame_min * 60 * 1000
        self.a_mercato = a_mercato
        self.symbol = symbol
        self.actual_index = starting_index
        self.actual_portafoglio = portafoglio
        self.exchange = exchange
        self.Api = API.API(exchange)

        self.state = "Attivo"
        
        #se a_mercato == False
        if not a_mercato:
            

            
            

            #TODO verificare nel database se si trovano le candele tra time_inizio e time_fine
            #TODO se non si trovano 
            if 1:
                self.candles = {}
                # scaricare tutte le candele necessarie 
                start_time_ms = self.time_inizio_int
                stop_time_ms = self.time_fine_int
                # calcola il numero di candele da scaricare
                diff_time_ms = stop_time_ms - start_time_ms
                self.number_of_candles_int = int(diff_time_ms/self.time_frame_ms)
                # calcola quanti loop ci vogliono per scaricare le candele.
                number_of_loop = int(self.number_of_candles_int/self.Api.limit_number_candles)+1
                # loop e scarica tutte le candele
                for i in range(0,number_of_loop):
                    # scarica candele dall'API
                    candles_tmp = self.Api.download_n_candles(symbol=self.symbol,time_frame=self.time_frame,stop_time=stop_time_ms)
                    # aggiorna la lista di candele in ram
                    self.candles = self.update_candles_in_ram(candles_tmp,self.candles)
                    
                    stop_time_ms = stop_time_ms-self.Api.limit_number_candles*self.time_frame_ms
                    

                # salvare tutte candele nel database
                with open(os.path.join("..","database",symbol + "_" + str(self.time_frame)+".json"), "w") as file:
                    json.dump(self.candles, file, indent=4)  # indent=4 rende il JSON leggibile
            
            # costruire una lista di dizionari (candles_list) che comprenda tutte le candele necessarie al simulatore indirizzate per interi
            self.candles_list = self.candles

            # definisce indice massimo
            self.max_index = len(self.candles_list.keys())-1
            

            # definisce una struttura ordini e una struttura portafoglio
            self.open_orders_and_equity = {}
            self.open_orders_and_equity[self.actual_index-1] = {}
            self.open_orders_and_equity[self.actual_index-1]["open_orders"] = []
            self.open_orders_and_equity[self.actual_index-1]["equity"] = portafoglio
            self.open_orders_and_equity[self.actual_index-1]["equity_in_USDT"] = self.compute_USDT(portafoglio,self.actual_index)

            # extract currency
            self.currency = self.Api.get_currency(self.symbol)
            self.open_orders_and_equity[self.actual_index-1]["equity"][self.currency] = 0
            

    def compute_USDT(self,portafoglio,actual_index):
        price = self.candles_list[actual_index]["o"]
        USDT = 0
        for key in portafoglio.keys():
            if key !="USDT":
                USDT += portafoglio[key]*price

        return USDT+portafoglio["USDT"]

    def update_candles_in_ram(self,new_candles,old_candles):

        candles = {}

        # aggiungi limit_number_candles a tutte le self.candles nella struttura per fare spazio alle prossime
        num_to_add = len(new_candles.keys())
        for key in old_candles.keys():
            candles[key+num_to_add] = old_candles[key]

        # appendi le new_candles nell' old_candles e ritorna candles
        candles = candles | new_candles

        return candles

    def translate_time_frame_in_min(self,time_frame):
        #1 3 5 15 30 60 120 240 360 720 (min) D (day) W (week) M (month)
        if time_frame == "D":
            return 60*24
        if time_frame == "W":
            return 60*24*7
        if time_frame == "M":
            return 60*24*7*30
        else:
            return int(time_frame)

    def wait_next_candle(self):
        # se a_mercato == False
        if self.a_mercato == False:
            #se l'indice attuale supera quello massimo mette lo stato a Morto
            if self.actual_index==self.max_index:
                self.state = "Morto"
                with open(os.path.join("..","result",datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"_"+self.name + "_"+self.symbol + "_" + str(self.time_frame)+".json"), "w") as file:
                    json.dump(self.open_orders_and_equity, file, indent=4)  # indent=4 rende il JSON leggibile

            # aggiorna lo stato di tutti gli ordini e del portafoglio
            self.open_orders_and_equity = self.update_orders_and_equity(self.open_orders_and_equity,self.actual_index)
            #TODO review the index logic

            # aggiunge solo 1 all indice attuale 
            self.actual_index += 1
        else:
            #TODO si inloopa un while aspettando che il websocket lo rilasci
            pass
        pass

    def update_orders_and_equity(self,dict_orders_and_equity,actual_index):
        # download the candle at actual_index 
        candle = self.candles_list[actual_index]
        high = candle["h"]
        low = candle["l"]

        # evaluate if min and max can close any open_orders
        
        dict_orders_and_equity[self.actual_index] = {}
        dict_orders_and_equity[self.actual_index]["open_orders"] = []
        dict_orders_and_equity[self.actual_index]["equity"] = {}
        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] = dict_orders_and_equity[self.actual_index-1]["equity"]["USDT"]
        dict_orders_and_equity[self.actual_index]["equity"][self.currency] = dict_orders_and_equity[self.actual_index-1]["equity"][self.currency]
        
        for order in dict_orders_and_equity[actual_index-1]["open_orders"]:
            if order["direction"] == "long":
                if order["type"] == "limit":
                    if low < order["price"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price"])*self.factor_limit_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] -= new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] += new_CURR
                    else:
                        #ordine non eseguito quindi aggiungo open_orders_and_equity[self.actual_index]["open_orders"]
                        dict_orders_and_equity[self.actual_index]["open_orders"].append(order)
                if order["type"] == "market":
                    if high > order["price"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price"])*self.factor_market_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] -= new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] += new_CURR
                    
                    else:
                        #ordine non eseguito quindi aggiungo open_orders_and_equity[self.actual_index]["open_orders"]
                        dict_orders_and_equity[self.actual_index]["open_orders"].append(order)
                if order["type"] == "SL_TP":
                    if high > order["price_SL"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price_SL"])*self.factor_market_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] -= new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] += new_CURR
                    elif low < order["price_TP"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price_TP"])*self.factor_limit_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] -= new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] += new_CURR
                    else:
                        #ordine non eseguito quindi aggiungo open_orders_and_equity[self.actual_index]["open_orders"]
                        dict_orders_and_equity[self.actual_index]["open_orders"].append(order)
            else:
                if order["type"] == "limit":
                    if high > order["price"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price"])*self.factor_limit_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] += new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] -= new_CURR
                    
                    else:
                        #ordine non eseguito quindi aggiungo open_orders_and_equity[self.actual_index]["open_orders"]
                        dict_orders_and_equity[self.actual_index]["open_orders"].append(order)
                if order["type"] == "market":
                    if low < order["price"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price"])*self.factor_market_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] += new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] -= new_CURR
                    else:
                        #ordine non eseguito quindi aggiungo open_orders_and_equity[self.actual_index]["open_orders"]
                        dict_orders_and_equity[self.actual_index]["open_orders"].append(order)
                if order["type"] == "SL_TP":
                    if low < order["price_SL"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price_SL"])*self.factor_market_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] += new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] -= new_CURR
                    elif high > order["price_TP"]:
                        # ordine eseguito quindi aggiorna portafoglio
                        new_USDT = order["qty_in_USDT"]
                        new_CURR = (order["qty_in_USDT"]/order["price_TP"])*self.factor_limit_tax
                        dict_orders_and_equity[self.actual_index]["equity"]["USDT"] += new_USDT
                        dict_orders_and_equity[self.actual_index]["equity"][self.currency] -= new_CURR
                    
                    else:
                        #ordine non eseguito quindi aggiungo open_orders_and_equity[self.actual_index]["open_orders"]
                        dict_orders_and_equity[self.actual_index]["open_orders"].append(order)
        dict_orders_and_equity[self.actual_index]["equity_in_USDT"] = self.compute_USDT(dict_orders_and_equity[self.actual_index]["equity"],self.actual_index)
        return dict_orders_and_equity

    def download_n_candles(self,symbol,n_candles,timeframe):
        candles_out = {}
        #se a_mercato == False
        if self.a_mercato == False:
            if timeframe == self.time_frame:
                # prendi le candele da candles_list e restituiscile
                keys = list(sorted(self.candles_list.keys()))[self.actual_index-n_candles+1:self.actual_index+1]
                candles = {k: self.candles_list[k] for k in keys}
                i = 0
                for key in sorted(candles.keys(),reverse=True):
                    candles_out[i] = candles[key]
                    i+=1
                if self.debug >0:
                    log(str(symbol))
                    log(str(n_candles))
                    log(str(timeframe))
                    log(str(candles_out))
        # se a_mercato == True
        if self.a_mercato == True:
            #TODO scarica candele
            #TODO formatta output come candles_list e restituiscile (ricordati che l'ordine dell'indice è invertito)
            pass
        return candles_out

    def compute_usdt_qty_corrected(self,order_qty_usdt):
        #TODO calcola qty_usdt effettivi
        return order_qty_usdt

    def open_market_long(self,symbol,abs_SL,abs_TP,order_qty_usdt):
        
        qty_usdt_corrected = self.compute_usdt_qty_corrected(order_qty_usdt)


        # se a_mercato == False
        if self.a_mercato ==False:
            price = self.candles_list[self.actual_index]["o"]
            qty_in_coin = qty_usdt_corrected/price
            # aggiorna stato ordini
            order = {}
            order["direction"] = "short"
            order["type"] = "SL_TP"
            order["price_TP"] = abs_TP
            order["price_SL"] = abs_SL
            order["qty_in_USDT"] = qty_usdt_corrected
            self.open_orders_and_equity[self.actual_index-1]["open_orders"].append(order)
            # aggiorna stato portafoglio
            new_USDT = qty_usdt_corrected
            new_CURR = (qty_usdt_corrected/price)*self.factor_market_tax
            self.open_orders_and_equity[self.actual_index-1]["equity"]["USDT"] -= new_USDT
            self.open_orders_and_equity[self.actual_index-1]["equity"][self.currency] += new_CURR
        
            
        # se a_mercato == True
        if self.a_mercato == True:
            #TODO manda ordine a mercato
            pass

    def open_market_short(self,symbol,abs_SL,abs_TP,order_qty_usdt):
        
        qty_usdt_corrected = self.compute_usdt_qty_corrected(order_qty_usdt)

        # se a_mercato == False
        if self.a_mercato ==False:
            price = self.candles_list[self.actual_index]["o"]
            qty_in_coin = qty_usdt_corrected/price
            # aggiorna stato ordini
            order = {}
            order["direction"] = "long"
            order["type"] = "SL_TP"
            order["price_TP"] = abs_TP
            order["price_SL"] = abs_SL
            order["qty_in_USDT"] = qty_usdt_corrected
            self.open_orders_and_equity[self.actual_index-1]["open_orders"].append(order)
            # aggiorna stato portafoglio
            new_USDT = qty_usdt_corrected
            new_CURR = (qty_usdt_corrected/price)*self.factor_market_tax
            self.open_orders_and_equity[self.actual_index-1]["equity"]["USDT"] += new_USDT
            self.open_orders_and_equity[self.actual_index-1]["equity"][self.currency] -= new_CURR
        
            
        # se a_mercato == True
        if self.a_mercato == True:
            #TODO manda ordine a mercato
            pass

    def finish(self):
        if self.a_mercato:
            return False
        else:
            if self.state == "Morto":
                return True
            else:
                return False

        pass