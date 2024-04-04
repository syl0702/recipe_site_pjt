import json
import pandas as pd 
import os

# json 파일 읽기

json_data_list = []

with open('json_log.log', 'r') as json_file:
    for line in json_file:
        json_data = json.loads(line)
        json_data_list.append(json_data)
        
df = pd.DataFrame(json_data_list)
df.asctime = pd.to_datetime(df.asctime)

df['time'] = pd.cut(df['asctime'].dt.hour,
                           bins=[0, 5, 10, 16, 22],
                           labels=['새벽', '아침', '점심', '저녁'],
                           include_lowest=True,
                           right=False)

target = df[df.modulename == 'detail'][['asctime','time', 'postid']]

target[target.time == '아침'].postid.value_counts().index


# print(df)
def time_recommend(now):
    recommended_index = target[target.time == 'now'].postid.value_counts().index
    return(recommended_index)