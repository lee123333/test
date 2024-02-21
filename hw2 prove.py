import pandas as pd
import time
t=time.perf_counter()
with open('spliced+UTRTranscriptSequence_Y40B10A.2a.1.fasta','r') as file:
    data=file.readlines()
#開始跟結束的位置    
data=data[1]

rank=[]
d=[1]
c=0
b=0
for i in range(len(data)):
    if c==0:
        if data[i].islower():
            b+=1
        elif data[i].isupper():
            rank.append(b)
            c=1
            b+=1
            d.append(b)
        
    
    elif c==1:
        if data[i].isupper():
            b+=1
        elif data[i].islower():
            rank.append(b)
            c=0
            b+=1 
            d.append(b)
                           
rank.append(len(data))
for i in range(len(data)):
    if data.islower():
        d.append(1)  
print(d)
if rank[0]==0:
    del rank[0]
if d[1]==1:
    del d[1]

 #換成dataframe的形式 算出長度 
if data[0].islower() and data[len(data)-1].islower():
    
    name=['5 UTR','CDS','3 UTR']
    df=pd.DataFrame(list(zip(name,d,rank)),columns=['name','start','end'])
    df['length']=df['end']-df['start']+1
elif data[0].isupper() and data[len(data)-1].islower():     
    
    name=['CDS','3 UTR']   
    df=pd.DataFrame(list(zip(name,d,rank)),columns=['name','start','end'])
    df['length']=df['end']-df['start']+1
elif data[0].islower() and data[len(data)-1].isupper():     
    
    name=['5 UTR','CDS']   
    df=pd.DataFrame(list(zip(name,d,rank)),columns=['name','start','end'])
    df['length']=df['end']-df['start']+1
else:     
    
    name=['CDS']   
    df=pd.DataFrame(list(zip(name,d,rank)),columns=['name','start','end'])
    df['length']=df['end']-df['start']+1

df=df.set_index('name')    
print(df)
df.to_csv('hw2_prove.csv')
e=time.perf_counter()
print(e-t)        
