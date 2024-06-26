from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
from pytz import timezone

# 데이터 가져올 곳 / 데이터 가져오기
def fetch_recipe_data():
    username = "multi01"
    password = "1111"
    host = "ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com"
    database_name = "recipe_db"

    db_connection_str = f'mysql+pymysql://{username}:{password}@{host}/{database_name}'
    db_connection = create_engine(db_connection_str)
    query = '''
    SELECT *
    FROM recipe_db.posts_rating;
    '''
    
    df = pd.read_sql(query, con=db_connection)
    
    return df

# 데이터 처리
def process_data(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='fetch_data_task')
    df = fetch_recipe_data()
    ratings_matrix = df.pivot_table('score', 'user_id', 'post_id')
    ratings_matrix.fillna(0, inplace=True)
    ratings_matrix_T = ratings_matrix.T
    item_sim = cosine_similarity(ratings_matrix_T, ratings_matrix_T)
    item_sim_df = pd.DataFrame(item_sim, index=ratings_matrix_T.index, columns=ratings_matrix_T.index)
    ti.xcom_push(key='item_sim_df', value=item_sim_df)

# 평점 예측
def predict_ratings(**kwargs):
    ti = kwargs['ti']
    item_sim_df = ti.xcom_pull(task_ids='process_data_task', key='item_sim_df')
    df = fetch_recipe_data()
    ratings_matrix = df.pivot_table('score', 'user_id', 'post_id')
    # MySQL 연결 정보 설정
    db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
    db_connection = create_engine(db_connection_str)
    ratings_matrix.to_sql(name='rating_matrix', con=db_connection, if_exists='replace', index=True) 
    ti.xcom_push(key='ratings_matrix', value=ratings_matrix)


def mk_matrix(**kwargs):
    ti = kwargs['ti']
    item_sim_df = ti.xcom_pull(task_ids='process_data_task', key='item_sim_df')
    item_sim_arr = item_sim_df.values
    ratings_matrix = ti.xcom_pull(task_ids='predict_ratings_task', key="ratings_matrix")
    ratings_matrix.fillna(0, inplace=True)
    ratings_matrix_T = ratings_matrix.T
    sum_sr = ratings_matrix.values @ item_sim_arr
    sum_s_abs = np.array([np.abs(item_sim_arr).sum(axis=1)])
    ratings_pred = sum_sr / sum_s_abs
    ratings_pred_matrix = pd.DataFrame(data=ratings_pred, index=ratings_matrix.index, columns=ratings_matrix_T.index)
    
    # MySQL 연결 정보 설정
    db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
    db_connection = create_engine(db_connection_str)
    ratings_pred_matrix.to_sql(name='rating_pred_matrix', con=db_connection, if_exists='replace', index=True) 


    

#############################################################################################

default_args = {
    'start_date': datetime(2023, 12, 26),
}

# DAG 정의
dag = DAG(
    dag_id="recipe-hj-rating-pipeline",
    schedule_interval='@hourly',  # 매일 새벽 4시, 트래픽 수 가장 낮음
    default_args=default_args,
    tags=["recipe", "soup"],
    catchup=False,
    start_date=datetime(2023, 12, 26, tzinfo=timezone('Asia/Seoul')),
)

# 1. 데이터 가져오기
fetch_data_task = PythonOperator(
    task_id='fetch_data_task',
    python_callable=fetch_recipe_data,
    dag=dag,
)

# 2. 데이터 처리하기(데이터 프레임)
process_data_task = PythonOperator(
    task_id='process_data_task',
    python_callable=process_data,
    provide_context=True,
    dag=dag,
)

# 3. 평점 예측하기(유사도 필터링)
predict_ratings_task = PythonOperator(
    task_id='predict_ratings_task',
    python_callable=predict_ratings,
    provide_context=True,
    dag=dag,
)

# 4. df 만들기 >> csv파일이 너무 많이 생기는거 방지하기
mk_matrix_task = PythonOperator(
    task_id='ratings_pred_matrix',
    python_callable=mk_matrix,
    provide_context=True,
    dag=dag,
)


# 5. 사용자에게 보여줄 레시피 추천을 위해 사용자가 아직 보지 않은 레시피 찾기
# get_unseen_recipes_task = PythonOperator(
#     task_id='get_unseen_recipes_task',
#     python_callable=get_unseen_recipes,
#     provide_context=True,
#     dag=dag,
# )



# # 6. CSV 파일로 저장
# def export_to_csv(**kwargs):
#     ti = kwargs['ti']
#     recomm_recipes = ti.xcom_pull(task_ids='get_unseen_recipes_task', key='unseen_list')
    
#     # List를 DataFrame으로 변환
#     df_unseen_list = pd.DataFrame(unseen_list)
    
#     # CSV 파일로 저장
#     df_unseen_list.to_csv('/home/ubuntu/airflow/unseen_recipes.csv', index=False)

# export_to_csv_task = PythonOperator(
#     task_id='export_to_csv_task',
#     python_callable=export_to_csv,
#     provide_context=True,
#     dag=dag,
# )



# # 5. 사용자에게 레시피 추천하기
# recomm_recipe_task = PythonOperator(
#     task_id='recomm_recipe_by_userid_task',
#     python_callable=recomm_recipe_by_userid,
#     provide_context=True,
#     dag=dag,
# )

# 태스크 간의 의존성 설정(한번에 진행 방지)
fetch_data_task >> process_data_task >> predict_ratings_task >> mk_matrix_task 
# predict_ratings_task >> get_unseen_recipes_task
# get_unseen_recipes_task >> recomm_recipe_task