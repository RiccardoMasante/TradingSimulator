import os,sys
import datetime
import time
from dateutil.relativedelta import relativedelta
sys.path.insert(0,os.getcwd() + r"/../lib")
import simulator
#now = datetime.datetime.now()
#print(int(time.time()*1000))
#print ("Current date and time : ")
#print (datetime.datetime.fromtimestamp(int(time.time()*1000) / 1000.0, tz=datetime.timezone.utc))
#print(type(datetime.datetime.fromtimestamp(int(time.time()*1000) / 1000.0, tz=datetime.timezone.utc)))
class strategia():
    def __init__(self,a_mercato,time_inizio=datetime.datetime.now()- relativedelta(days=1),time_fine=datetime.datetime.now(),time_frame=1,symbol="BTCUSDT",params={}):
        
        self.a_mercato = a_mercato
        #TODO aggiungere tutti i check di validita
        self.time_inizio = time_inizio
        self.time_fine = time_fine
        self.time_frame = time_frame
        self.symbol = symbol

        #params
        self.pmmv = self.check_params("pmmv",params,10)
        self.pmml = self.check_params("pmml",params,20)
        self.rel_SL = self.check_params("rel_SL",params,0.9)
        self.rel_TP = self.check_params("rel_TP",params,1.1)
        self.order_qty_usdt = self.check_params("order_qty_usdt",params,100)
        #TODO aggiungere tutti i check di validita
           

        # inizializzare il simulatore al tempo di inizio, con tutte le candele necessarie scaricate in RAM
        self.sim = simulator.Simulator(time_inizio,time_fine,time_frame,a_mercato,symbol,starting_index = self.pmml,portafoglio={"USDT":200},name="strategia_1")

        self.mml_value = 0
        self.mmv_value = 0
        self.mml_value_prev = 0
        self.mmv_value_prev = 0


    def check_params(self,value,dict,default_value):
        if value in dict.keys():
            return dict[value]
        else:
            return default_value

    def run(self):
        while(1):

            #aspetta chiusura candela
            self.sim.wait_next_candle()

            # se a_mercato == false interrogare il simulatore se abbiamo finito per chiudere il loop
            if self.a_mercato == False:
                if self.sim.finish():
                    break

            #scarica le ultime pmml candele
            candles = self.sim.download_n_candles(self.symbol,self.pmml,self.time_frame)
            
            #nello stesso loop
                #calcola media mobile veloce
                #calcola media mobile lenta
            temp_sum = 0
            #print(candles)
            for i in range(0,self.pmml):
                
                temp_sum+=candles[i]["o"]
                if i == self.pmmv-1:
                    self.mmv_value = temp_sum/self.pmmv
            self.mml_value = temp_sum/self.pmml

            #se la media mobile si è incrociata entrare a mercato con ordine e TP e SL definiti
            if self.mmv_value > self.mml_value and self.mmv_value_prev < self.mml_value_prev:
                # entra_long
                abs_TP = candles[0]["o"]*self.rel_TP
                abs_SL = candles[0]["o"]*self.rel_SL
                self.sim.open_market_long(self.symbol,abs_SL,abs_TP,self.order_qty_usdt)
                pass
            if self.mmv_value < self.mml_value and self.mmv_value_prev > self.mml_value_prev:
                # entra_short
                abs_TP = candles[0]["o"]/self.rel_TP
                abs_SL = candles[0]["o"]/self.rel_SL
                self.sim.open_market_short(self.symbol,abs_SL,abs_TP,self.order_qty_usdt)
                pass

            #salva valore precedente media mobile veloce
            self.mmv_value_prev = self.mmv_value
            #salva valore precedente media mobile lenta
            self.mml_value = self.mml_value

            



