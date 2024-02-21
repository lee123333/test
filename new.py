import pandas as pd
import time

t=time.perf_counter()
#read讀檔變字串
with open ('unspliced+UTRTranscriptSequence_Y40B10A.2a.1.fasta','r') as file:
    data=file.read()
#split後將檔名刪掉    
gene=data.split('\n')[1]
#將大小寫分開
value=''
name=''
for i in range(len(gene)):
   if gene[i].islower():
       value+=gene[i]
       if i==len(gene)-1:
        break  
       elif gene[i+1].isupper():
        value+='||'
        name+='l '
        
   elif gene[i].isupper():
       value+=gene[i]
       if i==len(gene)-1:
        break  
       elif gene[i+1].islower():
        name+='u '
        value+='||'
#split後變list的形式        
value=value.split('||')
name=name.split(' ')

#把第一個跟最後一個的名稱換掉
utr_5=0
utr_3=0
if gene[0].islower():
        name[0]='5'
        utr_5=1
if gene[len(gene)-1].islower():
        name[len(name)-1]='3'
        utr_3=1
elif gene[len(gene)-1].isupper():
        name[len(name)-1]='u'


#換成dataframe的形式
value=pd.DataFrame(value,columns=['100'])
value['name']=name
if  utr_5==1:
    value.loc[1,'100']=value.at[0,'100']+value.at[1,'100']
if utr_3==1:   
    value.loc[len(name)-2,'100']=value.at[len(name)-2,'100']+value.at[len(name)-1,'100']
#計算id長度
value['length']=value['100'].str.len()
print(value)


#找出start跟end的位置 同時改變name的名字
start=[]
end=[]
b=1
c=1
for i in range(len(value)):
    if utr_5==1 and utr_3==1:
        if value.at[i,'name']=='5':
            start.append(1)
            end.append(int(value.at[i,'length']))
            value.at[i,'name']='5 UTR'
        
        elif value.at[i,'name']=='u':
            start.append(end[i-1]+1)
            end.append(int(value.at[i,'length'])+start[i]-1)
            value.at[i,'name']='EXON'+str(b)
            b+=1
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
        
        elif value.at[i,'name']=='3':
            start.append(max(end)-int(value.at[i,'length'])+1)
            end.append(max(end))
            value.at[i,'name']='3 UTR'
    if utr_5==1 and utr_3==0:
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
    if utr_5==0 and utr_3==1:
            if value.at[i,'name']=='u' and i==0:
                start.append(1)
                end.append(int(value.at[i,'length']))
                value.at[i,'name']='EXON'+str(b)
                b+=1
            elif value.at[i,'name']=='u' and i!=0:
                start.append(end[i-1]+1)
                end.append(int(value.at[i,'length']))
                value.at[i,'name']='EXON'+str(b)
                b+=1
            elif value.at[i,'name']=='l':
                start.append(end[i-1]+1)
                end.append(int(value.at[i,'length'])+start[i]-1)
                value.at[i,'name']='Intron'+str(c)
                c+=1
            elif value.at[i,'name']=='3':
                start.append(max(end)-int(value.at[i,'length'])+1)
                end.append(max(end))
                value.at[i,'name']='3 UTR'
    if utr_5==0 and utr_3==0:
        if value.at[i,'name']=='u' and i==0:
                start.append(1)
                end.append(int(value.at[i,'length']))
                value.at[i,'name']='EXON'+str(b)
                b+=1
        elif value.at[i,'name']=='u' and i!=0:
                start.append(end[i-1]+1)
                end.append(int(value.at[i,'length']))
                value.at[i,'name']='EXON'+str(b)
                b+=1
        elif value.at[i,'name']=='l':
                start.append(end[i-1]+1)
                end.append(int(value.at[i,'length'])+start[i]-1)
                value.at[i,'name']='Intron'+str(c)
                c+=1


#插入start跟end 對表格做排序
value=value.assign(start=start,end=end)        
value=value.drop('100',axis=1) 
value=value.set_index('name')
value=value.reindex(columns=['start','end','length'])
print(value)    
e=time.perf_counter()
print(e-t)        
