import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

cols_to_read=['game_id', 'old_game_id','home_team','away_team','game_seconds_remaining', 'home_wp',
                'week','away_score','home_score']
df=pd.read_csv(r'C:\Users\hyder\Desktop\play_by_play_2021.csv',usecols=cols_to_read)
df['function']=0
df['time_passed']=0
df['function_avg']=0
df=df.drop_duplicates()
df=df.sort_index().reset_index(drop=True)

val=0
time_diff=0
for i in range(len(df)):
    if df.game_seconds_remaining[i]==3600:
        continue
    else:
        time_diff=abs(df.game_seconds_remaining[i-1]-df.game_seconds_remaining[i])
        val=abs(df.home_wp[i]-df.home_wp[i-1])
        df.loc[df.index[i],'function_avg']=val
        df.loc[df.index[i],'function']=val*time_diff
        df.loc[df.index[i],'time_passed']=time_diff
df=df[df.time_passed != 0]
df=df.sort_index().reset_index(drop=True)


xarr=[]
yarr=[]
time=0
for i in range(len(df)):
    if df.home_wp[i]==1 or df.home_wp[i]==0 or df.home_wp[i]==0.5:
        time+=df.time_passed[i]
        xarr.append(time)
        yarr.append(df.function_avg[i])
        plt.plot(xarr,yarr)
        plt.xlabel('Time Passed(Seconds)')
        plt.ylabel('Excitement')
        plt.ylim([0,0.74])
        plt.savefig('C:/Users/hyder/Desktop/pics/'+df.game_id[i]+'.png')
        plt.clf()
        time=0
        xarr.clear()
        yarr.clear()
    elif (df.time_passed[i]==600) or (df.time_passed[i]==900):
        time+=0
        xarr.append(time)
        yarr.append(df.function_avg[i])
    else:
        time+=df.time_passed[i]
        xarr.append(time)
        yarr.append(df.function_avg[i])


aggregation =df \
        .assign(total_time=lambda row: row["time_passed"].apply(lambda x: float(x)))\
        .assign(entertainment=lambda row: row["function"].apply(lambda x: float(x)))\
        .groupby(['game_id','home_team','away_team','week','home_score','away_score']) \
        .agg({
             'entertainment': 'sum',
             'total_time': 'sum'
            }) \
        .assign(total_time=lambda row: row["total_time"].apply(lambda x: float(x) if (x==3600 or x==4200) else float(x)-600))\
        .reset_index() 

aggregation['total_time_edited']=np.where((aggregation['week'].astype(int)>18) & (aggregation['total_time'].astype(int)>3600),aggregation['total_time'].astype(int)-300,aggregation['total_time'].astype(int))
aggregation['normalised_result']=(aggregation['entertainment']/aggregation['total_time_edited'])*3600
conditions = [
    (aggregation['week'] <19),
    (aggregation['week'] == 19),
    (aggregation['week'] ==20),
    (aggregation['week'] ==21),
    (aggregation['week'] ==22)
]
values = [aggregation['away_team']+" at "+aggregation['home_team']+", Week:"+aggregation['week'].astype(str),
            aggregation['away_team']+" at "+aggregation['home_team']+",Wildcard", 
            aggregation['away_team']+" at "+aggregation['home_team']+",Conference Semis", 
            aggregation['away_team']+" at "+aggregation['home_team']+",Conference Finals",
            aggregation['away_team']+" at "+aggregation['home_team']+",Super Bowl"]

aggregation['game']=np.select(conditions,values)

aggregation['Score']=(aggregation['home_team']+':'+aggregation['home_score'].astype(str)+" - "+aggregation['away_score'].astype(str)+":"+aggregation['away_team'])
aggregation['image']='https://raw.githubusercontent.com/haydersaad/nfl_excitement_pics/main/pics/'+aggregation['game_id']+'.png'

#df.to_csv(r'C:\Users\hyder\Desktop\file1.csv',index=False)
aggregation.to_csv(r'C:\Users\hyder\Desktop\file2.csv',index=False)