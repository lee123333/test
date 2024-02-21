dic={
    'TTT':'F','TTC':'F','TTA':'L',
    'TTG':'L','CTT':'L','CTC':'L',
    'CTA':'L','CTG':'L','ATT':'I',
    'ATC':'I','ATA':'I','ATG':'M',
    'GTT':'V','GTC':'V','GTA':'V',
    'GTG':'V','TCT':'S','TCC':'S',
    'TCA':'S','TCG':'S','CCT':'P',
    'CCC':'P','CCA':'P','CCG':'P',
    'ACT':'T','ACC':'T','ACA':'T',
    'ACG':'T','GCT':'A','GCC':'A',
    'GCA':'A','GCG':'A','TAT':'Y',
    'TAC':'Y','TAA':'','TAG':'',
    'CAT':'H','CAC':'H','CAA':'Q',
    'CAG':'Q','AAT':'N','AAC':'N',
    'AAA':'K','AAG':'K','GAT':'D',
    'GAC':'D','GAA':'E','GAG':'E',
    'TGT':'C','TGC':'C','TGA':'',
    'TGG':'W','CGT':'R','CGC':'R',
    'CGA':'R', 'CGG':'R','AGT':'S',
    'AGC':'S','AGA':'R','AGG':'R',
    'GGT':'G','GGC':'G','GGA':'G',
    'GGG':'G',         
}
import pandas as pd
with open('spliced+UTRTranscriptSequence_Y40B10A.2a.1.fasta','r') as file:
    data=file.readlines()

data=data[1]
emp=''
for i in range(len(data)):
    if data[i].isupper():
        emp+=data[i]
        if i+1==len(data):
            break
        elif data[i+1].islower():
            emp+='||'
    if data[i].islower():
        emp+=data[i]
        if i+1==len(data):
            break
        elif data[i+1].isupper():
            emp+='||'
data=emp.split('||')

if data[0].islower():
    del data[0]
if data[-1].islower():
    del data[-1]
b=''
for i in range(0,len(data[0]),3):   
    a=dic[data[0][i:i+3]]
    b+=a
lines = []
for i in range(0, len(b), 50):
    lines.append(b[i:i+50])
    c='\n'.join(lines)
print(c)
        
            
        

 


