import pandas as pd
import difflib
df=open('hw1_output_WS289.csv','r')
df1=open('hw1_prove.csv','r')

d=difflib.HtmlDiff()
h=d.make_file(df.readlines(),df1.readlines())
with open('diff.html','w') as f:
    f.write(h)


df.close()
df1.close()    

