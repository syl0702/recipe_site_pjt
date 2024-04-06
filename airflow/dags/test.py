from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from sqlalchemy import create_engine

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

def execute_query(**kwargs):
    df = fetch_recipe_data()
    ratings_matrix = df.pivot_table('score', 'user_id', 'post_id')
    ratings_matrix.fillna(0, inplace=True)
    ratings_matrix_T = ratings_matrix.T
    item_sim = cosine_similarity(ratings_matrix_T, ratings_matrix_T)
    item_sim_df = pd.DataFrame(item_sim, index=ratings_matrix_T.index, columns=ratings_matrix_T.index)
    
    return item_sim_df

def predict_rating(ratings_arr, item_sim_arr):
    df = fetch_recipe_data()
    ratings_matrix = df.pivot_table('score', 'user_id', 'post_id')
    ratings_matrix.fillna(0, inplace=True)
    ratings_matrix_T = ratings_matrix.T
    sum_sr = ratings_arr @ item_sim_arr
    sum_s_abs = np.array([np.abs(item_sim_arr).sum(axis=1)])
    ratings_pred = sum_sr / sum_s_abs
    ratings_pred_matrix = pd.DataFrame(data=ratings_pred, index = ratings_matrix.index, columns=ratings_matrix_T.index)
    return ratings_pred

def get_unseen_recipes(ratings_matrix, user_id):
    user_rating = ratings_matrix.loc[user_id, :]
    
    unseen_recipe_list = user_rating[user_rating == 0].index.tolist()
    recipes_list = ratings_matrix.columns.tolist()
    unseen_list = [recipe for recipe in recipes_list if recipe in unseen_recipe_list]
    
    return unseen_list

def recomm_recipe_by_userid(pred_df, user_id, unseen_list, top_n=2):
    recomm_recipes = pred_df.loc[user_id, unseen_list].sort_values(ascending=False)[:top_n]

    return recomm_recipes
    
default_args = {
    'start_date': datetime(2023, 12, 26),
}

with DAG(
    dag_id = "recipe-recom-pipelines",
    schedule_interval = "@hourly",
    default_args = default_args,
    tags=["recipes", "soups"],
    catchup=False ) as dag:
    
    # 1. 쌓인 데이터 가져오기
    bring_score = PythonOperator(
        task_id="execute_result",
        python_callable=fetch_recipe_data
    )
    
    # 2. 데이터 프레임으로 만들기
    score_to_df = PythonOperator(
        task_id="score_to_df",
        python_callable=execute_query
    )
    
    # 3. 코사인 유사도 및 협동 필터링
    collab_filter = PythonOperator(
        task_id="collab_filter",
        python_callable=predict_rating
    )
    
    # 4. 개인이 아직 안 본 레시피 가져오기
    bring_unseen = PythonOperator(
        task_id="bring_unseen",
        python_callable=get_unseen_recipes
    )
    
    # 5. 개인에게 추천해주기
    recommend_you = PythonOperator(
        task_id="recommend_you",
        python_callable=recomm_recipe_by_userid
    )
    
# 파이프라인화하기
bring_score >> score_to_df >> collab_filter >> bring_unseen >> recommend_you