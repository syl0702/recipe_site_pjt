import pandas as pd
import json
import os
from sqlalchemy import create_engine

db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
db_connection = create_engine(db_connection_str)

# json 파일 읽기

json_data_list = []

with open('json_log.json', 'r') as json_file:
    for line in json_file:
        json_data = json.loads(line)
        json_data_list.append(json_data)
        
df = pd.DataFrame(json_data_list)
# print(df)
# DataFrame을 MySQL 테이블에 삽입
df.to_sql(name='log_data', con=db_connection, if_exists='replace', index=False)


# os.remove('json_log.json')