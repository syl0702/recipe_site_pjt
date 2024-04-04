import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os
from sqlalchemy import create_engine


# def load_user_recom(user_id):
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     r_df = pd.read_csv(f'/home/ubuntu/airflow/dags/csv/recom_matrix_{current_date}.csv', index_col=0)
#     m_df = pd.read_csv(f'/home/ubuntu/airflow/dags/csv/recom_result_{current_date}.csv', index_col=0)
#     m_df.fillna(0, inplace=True)
    

#     # user_rating: user_id의 레시피 평점 정보
#     if user_id not in m_df.index:
#         return '별점 없음'  # 사용자 ID가 존재하지 않으면 '별점 없음' 반환

#     user_rating = m_df.loc[user_id, :]

#     # user_rating=0인 아직 안 본 레시피
#     unseen_recipe_list = user_rating[user_rating == 0].index.tolist()

#     # 모든 레시피를 list 객체로 만든다.
#     recipes_list = m_df.columns.tolist()

#     # 안 본 레시피 리스트 생성
#     unseen_list = [recipe for recipe in recipes_list if recipe in unseen_recipe_list]
#     top_n = 5
#     recomm_recipes = r_df.loc[user_id, unseen_list].sort_values(ascending=False)[:top_n]
#     recomm_recipes_list = list(map(int, recomm_recipes.index.tolist()))

#     return recomm_recipes_list


def load_user_recom2(user_id):
    ## sql에서 데이터 받아오기
    db_connection_str = 'mysql+pymysql://multi01:1111@ec2-15-168-111-154.ap-northeast-3.compute.amazonaws.com:3306/recipe_db'
    db_connection = create_engine(db_connection_str)
    query_rating = '''
    SELECT *
    FROM recipe_db.rating_matrix;
    '''
    query_rating_pred = '''
    SELECT *
    FROM recipe_db.rating_pred_matrix;
    '''
    
    r_df = pd.read_sql(query_rating, con=db_connection, index_col='user_id')
    m_df = pd.read_sql(query_rating_pred, con=db_connection, index_col='user_id')
    # r_df = pd.read_csv(f'/home/ubuntu/airflow/dags/csv/recom_matrix_{current_date}.csv', index_col=0)
    # m_df = pd.read_csv(f'/home/ubuntu/airflow/dags/csv/recom_result_{current_date}.csv', index_col=0)
    m_df.fillna(0, inplace=True)

    # user_rating: user_id의 레시피 평점 정보
    if user_id not in m_df.index:
        return '별점 없음'  # 사용자 ID가 존재하지 않으면 '별점 없음' 반환

    user_rating = m_df.loc[user_id, :]

    # user_rating=0인 아직 안 본 레시피
    unseen_recipe_list = user_rating[user_rating == 0].index.tolist()

    # 모든 레시피를 list 객체로 만든다.
    recipes_list = m_df.columns.tolist()

    # 안 본 레시피 리스트 생성
    unseen_list = [recipe for recipe in recipes_list if recipe in unseen_recipe_list]
    top_n = 4
    recomm_recipes = r_df.loc[user_id, unseen_list].sort_values(ascending=False)[:top_n]
    recomm_recipes_list = list(map(int, recomm_recipes.index.tolist()))

    return recomm_recipes_list
