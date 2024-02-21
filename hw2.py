import pandas as pd
import time

t=time.perf_counter()
#read讀檔變字串
with open ('C:/Users/lee haohsiang/Downloads/unspliced+UTRTranscriptSequence_Y40B10A.2a.1.fasta','r') as file:
    data=file.read()
#split後將檔名刪掉    
gene=data.split('\n')[1]
#將大小寫分開
value=''
ss=''
for i in range(len(gene)):
   if gene[i].islower():
       value+=gene[i]
       if i==len(gene)-1:
        break  
       elif gene[i+1].isupper():
        value+='||'
        ss+='l '
        
   elif gene[i].isupper():
       value+=gene[i]
       if i==len(gene)-1:
        break  
       elif gene[i+1].islower():
        ss+='u '
        value+='||'
#split後變list的形式        
value=value.split('||')
ss=ss.split(' ')
#把第一個跟最後一個的名稱換掉
for i in range(len(ss)):
    if i==0:
        ss[i]='5'
    if i==len(ss)-1:
        ss[8]='3'

#換成dataframe的形式
value=pd.DataFrame(value,columns=['100'])
value['name']=ss
value.loc[1,'100']=value.at[0,'100']+value.at[1,'100']
value.loc[7,'100']=value.at[7,'100']+value.at[8,'100']
#計算id長度
value['length']=value['100'].str.len()

#找出start跟end的位置 同時改變name的名字
start=[]
end=[]
b=1
c=1
for i in range(len(value)):
    if value.at[i,'name']=='5':
        start.append(1)
        end.append(int(value.at[i,'length']))
        value.at[i,'name']='5 UTR'
    elif value.at[i,'name']=='u' and value.at[i,'100'][0].islower() :
        start.append(1)
        end.append(int(value.at[i,'length']))
        value.at[i,'name']='EXON'+str(b)
        b+=1
    elif value.at[i,'name']=='l':
        start.append(end[i-1]+1)
        end.append(int(value.at[i,'length'])+start[i]-1)
        value.at[i,'name']='Intron'+str(c)
        c+=1
    elif value.at[i,'name']=='u'and value.at[i,'100'][0].isupper():
        start.append(end[i-1]+1)
        end.append(int(value.at[i,'length'])+start[i]-1)
        value.at[i,'name']='EXON'+str(b)
        b+=1
    elif value.at[i,'name']=='3':
        start.append(max(end)-int(value.at[i,'length'])+1)
        end.append(max(end))
        value.at[i,'name']='3 UTR'
#插入start跟end 對表格做排序
value=value.assign(start=start,end=end)        
value=value.drop('100',axis=1) 
value=value.set_index('name')
value=value.reindex(columns=['start','end','length'])
print(value)    
e=time.perf_counter()
print(e-t)        
