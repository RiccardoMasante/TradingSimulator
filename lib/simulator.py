class Simulator():
    def __init__(self,time_inizio,time_fine,time_frame,a_mercato,symbol,starting_index,portafoglio):
        self.time_inizio_int = time_inizio.timestamp()
        self.time_fine_int = time_fine.timestamp()
        self.time_frame = time_frame
        self.time_frame_min = self.translate_time_frame_in_min(time_frame)
        self.a_mercato = a_mercato
        self.symbol = symbol
        self.actual_index = starting_index
        self.actual_portafoglio = portafoglio

        self.state = "Attivo"
        
        #se a_mercato == False
        if not a_mercato:
            #TODO definisce indice massimo
            self.max_index = int((self.time_fine_int-self.time_inizio_int)/60/self.time_frame_min)

            #TODO verificare nel database se si trovano le candele tra time_inizio e time_fine
            #TODO se non si trovano 
                #TODO scaricare tutte le candele necessarie e salvarle nel database
            
            #TODO costruire una lista di dizionari (candles_list) che comprenda tutte le candele necessarie al simulatore indirizzate per interi
            
            #TODO definisce una struttura ordini
            #TODO definisce una struttura portafoglio

    def translate_time_frame_in_min(time_frame):
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
        #TODO se a_mercato == False
            #TODO aggiunge solo 1 all indice attuale 
            #se l'indice attuale supera quello massimo mette lo stato a Morto
            if self.actual_index>self.max_index:
                self.state = "Morto"
            #TODO aggiorna lo stato di tutti gli ordini
            #TODO aggiorna lo stato del portafoglio
        #TODO altrimenti
            #TODO si inloopa un while aspettando che il websocket lo rilasci
        pass

    def download_n_candles(self,symbol,n_candles,timeframe):
        #TODO se a_mercato == False
            #TODO prendi le candele da candles_list e restituiscile
        #TODO se a_mercato == True
            #TODO scarica candele
            #TODO occhio a togliere sempre la prima candela (non completata)
            #TODO formatta output come candles_list e restituiscile
        pass

    def open_market_long(self,symbol,rel_SL,rel_TP,order_qty_usdt):
        #TODO se a_mercato == False
            #TODO aggiorna stato ordini
            #TODO aggiorna stato portafoglio
        #TODO se a_mercato == True
            #TODO manda ordine a mercato
        pass

    def open_market_short(self,symbol,rel_SL,rel_TP,order_qty_usdt):
        #TODO se a_mercato == False
            #TODO aggiorna stato ordini
            #TODO aggiorna stato portafoglio
        #TODO se a_mercato == True
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