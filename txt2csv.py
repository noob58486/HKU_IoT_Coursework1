#This is a function used to convert the txt dataset to csv format


import pandas as pd

def txt2csv(txt_path,csv_path):
    data=[]
    tp=txt_path
    cp=csv_path
    with open(tp,'r') as file:
     for line in file:
         line =line.strip()
         values=line.split(',')
         if len(values)==25:
             row=list(map(float,values[:24]))+[int(values[24])]
         elif len(values)==24:
             row=list(map(float,values))
         data.append(row)
    if len(data[0])==24:
        columns=[f"hour_{i+1}" for i in range(24)]
    elif len(data[0])==25:
        columns=[f"hour_{i+1}" for i in range(24)]+["status"]
    df=pd.DataFrame(data,columns=columns)

    df.to_csv(cp,index=False)
    print('successful!')