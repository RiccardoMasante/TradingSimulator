import os,sys
sys.path.insert(0,os.getcwd()+ r"/../strategie")
from strategia_1 import strategia


os.environ["DEBUG"] = "0"

#__init__(self,a_mercato,time_inizio=datetime.datetime.now()- relativedelta(months=2),time_fine=datetime.datetime.now(),time_frame=1,symbol="BTCUSDT",params={}):
        
s = strategia(a_mercato = False)
s.run()