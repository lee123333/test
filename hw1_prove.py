import pandas as pd
import time
import gzip

t=time.perf_counter()
#開啟檔案
with gzip.open('c_elegans.PRJNA13758.WS289.mRNA_transcripts.fa.gz', 'rb') as file:
    data=file.read()

#用>做分割，變成list
data=data.decode().split(">")
data=pd.DataFrame(data,columns=['id'])
data=data.drop(0,axis=0)

#用split做出其他的欄位
data['transcript_ID']=data['id'].str.split().str.get(0)    
data['Gene_ID']=data['id'].str.split('=').str.get(1)
data['Gene_ID']=data['Gene_ID'].str.split('\n').str.get(0)


tran=data.groupby('Gene_ID').agg(transcript_ID=('transcript_ID',list),transcript_number=('transcript_ID',len))
tran = tran.rename(columns={'transcript_number': '# of transcripts'})

#print(tran)

tran.to_csv('hw1_prove.csv')
e=time.perf_counter()
print(e-t) 
#df_hw1 = pd.read_csv('hw1_prove.csv')
#df_ans = pd.read_csv('hw1_output_WS289.csv')
#print(df_hw1.equals(df_ans))       
