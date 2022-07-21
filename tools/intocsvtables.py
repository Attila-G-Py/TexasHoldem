import pandas as pd
import itertools



def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

files = ["raw1.txt","raw2.txt","raw3.txt","raw4.txt","raw5.txt"]
targets=["tables1.csv","tables2.csv","tables3.csv","tables4.csv","tables5.csv"]
for (n,m) in zip(files,targets):
    maxline=file_len(n)
    status=1
    data = open(n,"r")
    dataf = pd.DataFrame(columns=["TimeStamp","GameType","BigBlind","Table","Date","PlayerCount","TotalPot","Dealer","Board","Ante","1on1"])
    lines = data.readlines()

    i=0
    index=1
    while i < maxline:
        list = str(lines[i])
        list = list.split(" ")

        antemod=0
        onevsonemod=0

        if status == 1:
            if "ante" in list:
                antemod +=2
                dataf.loc[str(index), "Ante"]=list[7]
            else:
                dataf.loc[str(index), "Ante"]=False
            if "(1"and"1)" in list:
                onevsonemod +=3
                dataf.loc[str(index),"1on1"] = True
                dataf.loc[str(index), "GameType"] = list[2] + list[7] + list[8]
                dataf.loc[str(index), "BigBlind"] = list[9][1:]
            else:
                if "ante" in list:
                    dataf.loc[str(index), "BigBlind"] = list[6][1:-1]
                else:
                    dataf.loc[str(index), "BigBlind"] = list[6][1:]

                dataf.loc[str(index), "1on1"] = False
                dataf.loc[str(index), "GameType"] = list[2] + list[4] + list[5]
            dataf.loc[str(index), "TimeStamp"] = list[1][1:11]
            dataf.loc[str(index), "Date"] = list[8+antemod+onevsonemod]+list[9+antemod+onevsonemod]+list[10+antemod+onevsonemod]
            status +=1

        elif status ==2:
            temp=0
            for j in list:
                if j[0]=="(":
                    if temp==2:
                        dataf.loc[str(index), "Table"] = list[1]
                        dataf.loc[str(index), "Dealer"] = list[5][1]
                    elif temp==3:
                        dataf.loc[str(index), "Table"] = list[1] + " " + list[2]
                        dataf.loc[str(index), "Dealer"] = list[6][1]
                    else:
                        print("Table Name Error",j,temp,list)
                    break
                temp+=1
            status+=1

        elif status ==3:
            if "chips)\n" in list:
                if pd.isnull(dataf.loc[str(index), "PlayerCount"]):
                     dataf.loc[str(index), "PlayerCount"] = 1
                else:
                    dataf.loc[str(index)].PlayerCount +=1
            else:
                status+=1
                i-=1
        elif status ==4:
            if not "Ante" in list:
                status+=1
                i-=1
        elif status ==5:
            if "SUMMARY" == list[1]:
                status+=1
        elif status ==6:
            dataf.loc[str(index),"TotalPot"]=list[1][5:-1]
            if dataf.loc[str(index)].TotalPot.endswith(")"):
                dataf.loc[str(index), "TotalPot"] = list[1][5:-2]
            status+=1
        elif status==7:
            if "Board" == list[0]:
                temp=0
                for elem in list[1:]:
                    temp+=1
                list[1]=list[1][1:]
                list[temp]=list[temp][:2]
                dataf.loc[str(index),"Board"]= list[1:]
            status +=1
        elif status==8:
            if list[0]=="Stage":
                status=1
                index+=1
                i-=1
        i+=1

    dataf.to_csv(m)
