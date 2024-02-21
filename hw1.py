import pandas as pd
import openpyxl
import time
import gzip
start=time.perf_counter()
#開啟檔案
with gzip.open('c_elegans.PRJNA13758.WS289.mRNA_transcripts.fa.gz', 'rb') as file:
    data=file.read()

#用>做分割，變成list
data=data.decode().split(">")
data=pd.DataFrame(data,columns=['id'])
data=data.drop(0,axis=0)

#用split做出其他的欄位
data['tran id']=data['id'].str.split().str.get(0)
data['gene id']=data['id'].str.split('=').str.get(1)
data['gene id']=data['gene id'].str.split('\n').str.get(0)

tran=data.groupby('gene id').agg(tran_id=('tran id','|'.join),tran_id_number=('tran id',len))
tran.to_csv('hw1.csv')

end=time.perf_counter()
print(end-start)
  