import pandas as pd

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
files = ["raw1.txt","raw2.txt","raw3.txt","raw4.txt","raw5.txt"]
csvs=["players1.csv","players2.csv","players3.csv","players4.csv","players5.csv"]
results=["1p.csv","2p.csv","3p.csv","4p.csv","5p.csv"]

for (l,n,m) in zip(files,csvs,results):
    maxline=file_len(l)
    errors = []

    status=1
    data = open(l,"r")
    df = pd.DataFrame(columns=["TimeStamp","PlayerName","StartChips","Seat","PC","PCVal","Flop","FlopVal","Turn","TurnVal","River","RiverVal","Cards"])
    lines = data.readlines()
    dataf = pd.read_csv(n)
    d=0
    index=1
    while d < maxline:
        try:
            list = str(lines[d])
            list = list.split(" ")

            if status==1:
                playerc = dataf.loc[dataf[dataf['TimeStamp'] == int(list[1][1:11])].index.item()].PlayerCount
                currentTimeStamp=int(list[1][1:11])
                for i in range(playerc):
                    e = str(i+index)
                    df.loc[e, "TimeStamp"] = currentTimeStamp
                status+=1
                d+=1
            elif status==2:
                for i in range(playerc):
                    list = str(lines[d])
                    list = list.split(" ")
                    e = str(i + index)
                    df.loc[e,"Seat"] =  list[1]
                    df.loc[e,"PlayerName"] = list[3]
                    df.loc[e,"StartChips"] = list[4][2:]
                    d+=1
                tempdf = df[df["TimeStamp"] == currentTimeStamp]
                d-=1
                index += playerc+1
                status+=1
            elif status==3:

                if list[2] == "Ante":
                    playeri = tempdf[tempdf['PlayerName'] == list[0]].index.item()
                    if list[3] == "returned":
                        df.loc[playeri, "PCVal"] = False
                    else:
                        df.loc[playeri,"PCVal"] = float(list[3][1:-1])
                elif list[2] == "Posts":
                    playeri = tempdf[tempdf['PlayerName'] == list[0]].index.item()
                    if list[3] == "small" or list[3] == "big":
                        if pd.isnull(df.loc[playeri,"PCVal"]):
                            df.loc[playeri,"PCVal"] = float(list[5][1:-1])
                        else:
                            df.loc[playeri,"PCVal"] = df.loc[playeri,"PCVal"] + float(list[5][1:-1])
                    elif list[3] == "dead":
                        if pd.isnull(df.loc[playeri, "PCVal"]):
                            df.loc[playeri, "PCVal"] = float(list[4][1:])
                        else:
                            df.loc[playeri, "PCVal"] = df.loc[playeri, "PCVal"] + float(list[4][1:])
                    else:
                        if pd.isnull(df.loc[playeri, "PCVal"]):
                            df.loc[playeri, "PCVal"] = float(list[3][1:-1])
                        else:
                            df.loc[playeri, "PCVal"] = df.loc[playeri, "PCVal"] + float(list[3][1:-1])

                elif "POCKET"  == list[1]:
                    status+=1
            elif status==4:

                if not "***"  == list[0]:
                    dealer = dataf.loc[dataf[dataf['TimeStamp'] == currentTimeStamp].index.item()].Dealer
                    def actions(x,y):
                        playeri = tempdf[tempdf['PlayerName'] == list[0]].index.item()
                        if list[2] == "Folds\n":
                            if  pd.isnull(df.loc[playeri, x]):
                                df.loc[playeri, x]="fo"
                            else:
                                df.loc[playeri, x]= df.loc[playeri, x]+"fo"

                        elif list[2] == "Checks\n":
                            df.loc[playeri, x] = "ch"

                        elif list[2] == "Calls":
                            if pd.isnull(df.loc[playeri, x]):
                                df.loc[playeri, x] = "ca"
                            else:
                                df.loc[playeri, x] = df.loc[playeri,x] + "ca"
                            if pd.isnull(df.loc[playeri, y]):
                                df.loc[playeri, y] = float(list[3][1:-1])
                            else:
                                df.loc[playeri,y] = df.loc[playeri,y],float(list[3][1:])

                        elif list[2] == "Raises" or list[2] == "All-In(Raise)":
                            if pd.isnull(df.loc[playeri, x]):
                                df.loc[playeri, x] = "ra"
                            else:
                                df.loc[playeri,x] = df.loc[playeri, x] + "ra"
                            if pd.isnull(df.loc[playeri, y]):
                                df.loc[playeri,y] = float(list[3][1:])
                            else:
                                df.loc[playeri,y] = df.loc[playeri,y],float(list[3][1:])

                        elif list[2] == "Bets" or list[2] == "All-In":
                            df.loc[playeri, x] = "be"
                            df.loc[playeri,y] = float(list[3][1:-1])

                        elif list[2] == "returned":
                            df.loc[playeri, y] = df.loc[playeri,y],float(list[3][2:-1])*-1

                    actions("PC","PCVal")

                elif "FLOP" == list[1]:
                    status += 1
                elif "SHOW" == list[1]:
                    status+=4
            elif status==5:
                if not "***" == list[0]:
                    actions("Flop","FlopVal")

                elif "TURN" == list[1]:
                    status += 1
                elif "SHOW" == list[1]:
                    status+=3

            elif status == 6:
                if not "***" == list[0]:
                    actions("Turn","TurnVal")

                elif "RIVER" == list[1]:
                    status+=1
                elif "SHOW" == list[1]:
                    status+=2
            elif status == 7:
                if not "***" == list[0]:
                    actions("River","RiverVal")

                elif "SHOW" == list[1]:
                    status+=1
            elif status == 8:
                if "Shows" == list[2]:
                    playeri = tempdf[tempdf['PlayerName'] == list[0]].index.item()
                    df.loc[playeri,"Cards"] = list[3][1:],list[4][:-1]
                if "Collects" == list[1]:
                    playeri = tempdf[tempdf['PlayerName'] == list[0]].index.item()
                    if pd.isnull(df.loc[playeri, "Cards"]):
                        df.loc[playeri,"Cards"] = list[2][1:]
                    else:
                        df.loc[playeri, "Cards"] = df.loc[playeri, "Cards"],float(list[2][1:])
                elif "SUMMARY" == list[1] :
                    status+=1
            elif status == 9:
                if "Stage" == list[0]:
                    d-=1
                    status = 1
        except:
            for i in reversed(lines[:d]):
                if i.find("Stage") != -1:
                    errors.append(i[7:17])
                    break
        d+=1
    print(set(errors))
    for i in set(errors):
        mask = df['TimeStamp'] == int(i)
        df = pd.concat([df,df[mask]]).drop_duplicates(keep=False)
        mask1 = dataf['TimeStamp'] == int(i)
        dataf = pd.concat([dataf,dataf[mask1]]).drop_duplicates(keep=False)

    df.to_csv(m)
    dataf.to_csv(n)
