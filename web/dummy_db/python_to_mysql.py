import pandas as pd
from sqlalchemy import create_engine

# MySQL 연결 정보 설정
db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
db_connection = create_engine(db_connection_str)

# CSV 파일 경로
csv_file_path = '/home/ubuntu/web/posts_ingred.csv'

# CSV 파일을 DataFrame으로 읽기
df = pd.read_csv(csv_file_path)

# DataFrame을 MySQL 테이블에 삽입
df.to_sql(name='posts_ingred', con=db_connection, if_exists='append', index=False)

# posts_post
# import pandas as pd
# from sqlalchemy import create_engine

# # MySQL 연결 정보 설정
# db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
# db_connection = create_engine(db_connection_str)

# # CSV 파일 경로
# csv_file_path = '/home/ubuntu/web/dummy_db/posts_post.csv'

# # CSV 파일을 DataFrame으로 읽기
# df = pd.read_csv(csv_file_path)

# # DataFrame을 MySQL 테이블에 삽입
# df.to_sql(name='posts_post', con=db_connection, if_exists='append', index=False)





# user
# import pandas as pd
# from sqlalchemy import create_engine

# # MySQL 연결 정보 설정
# db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
# db_connection = create_engine(db_connection_str)

# # CSV 파일 경로
# csv_file_path = '/home/ubuntu/web/dummy_db/user.csv'

# # CSV 파일을 DataFrame으로 읽기
# df = pd.read_csv(csv_file_path)

# # DataFrame을 MySQL 테이블에 삽입
# df.to_sql(name='accounts_user', con=db_connection, if_exists='append', index=False)


import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, MetaData, insert, update, delete

# # # MySQL 연결 정보 설정
# db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
# db_connection = create_engine(db_connection_str, echo=True)
# # session = Session(db_connection)

# table_name = 'posts_post'
# query = f'SELECT * FROM {table_name}'
# df = pd.read_sql(query, con=db_connection)
# for i in range(1, 3):
#     df.loc[i-1, 'image'] = f'image/post/{i}.jpg'
# df.to_sql(name=table_name, con=db_connection, index=False, if_exists='replace')

# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=db_connection)
# db = SessionLocal()



# # CSV 파일 경로
# csv_file_path = '/home/ubuntu/web/dummy_db/posts_recipeingred.csv'

# # CSV 파일을 DataFrame으로 읽기
# df = pd.read_csv(csv_file_path)

# # DataFrame을 MySQL 테이블에 삽입
# df.to_sql(name='posts_recipeingred', con=db_connection, if_exists='append', index=False)

# posts_post = Table("posts_post", metadata_obj, autoload_with=db_connection)
# for id in range(1,3):
#     stmt = (
#         update(posts_post)
#         .where(posts_post.c.image == "default.jpg")
#         .values(image=f"image/post/{id}.jpg")
#     )
#     db.execute(stmt)
#     db.commit()
# db.close()

# import pymysql

# connection = pymysql.connect(
# 		host='ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com',            # 접속할 mysql server의 주소
# 		port='3306',        # 접속할 mysql server의 포트 번호
# 		user='multi01',     
# 		passwd='1111',
# 		db='recipe_db'         # 접속할 database명
# 	        # 'utf8' 등 문자 인코딩 설정 (한글 데이터가 깨지지 않도록)
# )

# cursor = connection.cursor()

# query = 'UPDATE posts_post SET image = '

## DB에서 데이터 가져오기 
# db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
# db_connection = create_engine(db_connection_str)
# query = '''
# SELECT *
# FROM recipe_db.posts_rating;
# '''

