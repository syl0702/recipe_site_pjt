# Multi Recipe Project
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/b17d3602-a7f3-4bd2-86c2-436a3fc305cd)

- Project 기간 : 2023-12-01 ~ 2024-01-05
- 프로젝트 목표 : 이미지를 익숙하게 여기는 2030대를 타겟으로 하는 레시피 사이트를 만들자!
- 프로젝트 참가자 및 담당 업무
    - **이서연** : 팀장/크롤링/데이터 분석/CNN, 취향테스트기반 추천, FastText모델링 및 모듈화/Airflow 파이프라인 구현/보고서
    - 강민주 : 웹 구성 및 모델링 연결/로그 데이터 생성/Spark Streaming/발표
    - 김현정 : 웹 구성/ 로그 데이터 기반 추천 서비스 구현/Open Dashboard/포트폴리오 자료 생성
    - 표상훈 : 크롤링/데이터 분석/ CNN, 취향테스트기반 추천, FastText 모델링 및 모듈화/Airflow 파이프라인 구현/발표자료

## Git 소개
- files : 포트폴리오 pdf 파일/사이트 스토리 보드
- module : 사이트 내에서 사용된 module 코드
    - category_recom.ipynb : 고객의 별점 데이터 기반으로 한 아이템 협업 필터링 모듈
    - cnn_extract_module.ipynb : cnn 기반의 게시글 작성 이미지와 유사 이미지의 레시피 및 카테고리 추출 모듈
    - cnn_module.ipynb : 이미지 인식 기반 검색 시스템 모듈
    - FastText.ipynb : FastText 모델 기반 유사 검색어 추출 (본 사이트에서는 사용하지 않음.)
    - 취향테스트기반추천.ipynb : 회원가입시 취향 테스트 기반의 추천 시스템 모듈

- web : 사이트 장고 코드
---
## Tech
<img src= "https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src= "https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white"> <img src= "https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src= "https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"> <img src= "https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white">


## Workflow
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/719f186c-eb2e-4a1c-a071-ae38e46eba2b)

## 데이터 수집 및 분석
- 한식/일식/양식/기타 각 50개 레시피 크롤링
- 게시글 제목 분석에 따른 음식 분류
- 레시피 제목, 재료 및 용량, 단계, 인분 정보 수집
- 데이터 전처리 후 웹사이트의 ERD 구조 고려해 정보/재료/단계 각각 csv 파일로 정리
- 카테고리별 휴먼 레이블링을 통해 분류 진행
- 레시피 제목 이모티콘, 특수문자 제거

## 모델 선택 및 구현
- 취향 테스트: 사용자가 회원가입 후 선택한 음식 세 가지 기반 취향을 분석해 레시피 맞춤 추천
- 별점 기반 추천: 현재 로그인한 유저가 남긴 별점을 기준으로 협업 필터링을 진행해 모델을 통한 레시피 추천
- CNN- 레시피 검색: 이미지 딥러닝 모델을 학습시켜 사용자가 올린 이미지에 해당하는 음식 레시피 도출
- CNN- 게시글 자동완성: 음식 레시피를 도출 후 가장 별점이 높은 레시피의 카테고리, 재료를 자동으로 작성

### 취향 테스트 모델링 (자세한 사항은 module 폴더의 취향테스트기반추천.ipynb 참고)
- 음식 별 세 종류 카테고리 기준 유사도 계산
- 사용자가 선택한 세 가지 음식을 바탕으로 레시피 추천.
- 음식 선택 후 추천 레시피 제공 기능 구현에 성공함.
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/7f465c45-149c-43c8-b415-71fa6e692604)
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/0a3103a8-426a-4d06-89c6-7e91ae46622e)

## 별점 기반 추천 (자세한 사항은 module 폴더의 category_recom.ipynb 참고)
- 사용자가 게시글에 준 별점 데이터를 pivot table로 생성해 게시글 간의 유사도를 계산 후 예측 평점 함수 계산.
- 사용자 맞춤 레시피 추천 모델 구현에 성공함.
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/b4e42d07-3727-4a42-9235-8c15f103f065)
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/330ee485-12e7-40a6-82fe-5b99ca138dee)

## CNN - 레시피 검색 (자세한 사항은 module 폴더의 cnn_module.ipynb 참고)
- 구글링을 통해 모은 약 1500장의 이미지 학습 후 CNN ResNet50 최적 모델을 구현함.
- 이미지 검색 후 레시피 호출 기능 구현에 성공함.
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/8340a925-c8e8-4224-83fd-700013129a67)

![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/6da9cbbd-d4bd-45d1-8e61-4325e24f5809)
- 정확도 80%/ 이러한 결과 값을 기반으로 사이트 내에서 파스타 카테고리 레시피가 검색이 된다.
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/9d606927-26fc-4f95-9122-f99121ed1afc)

## CNN - 게시글 자동 완성 (자세한 사항은 module 폴더의 cnn_extract_module 참고)
- 사용자가 게시글을 작성할 때 사용할 이미지를 업로드하면, 이를 인식 후 해당되는 카테고리 레시피를 검색.
- 재료 및 용량은 사용자가 자유롭게 작성하도록 둠.
- 별점이 가장 높은 레시피의 재료와 카테고리를 자동으로 추출함.
![image](https://github.com/syl0702/multi_recipe_pjt/assets/140361641/e619519d-6e70-430e-8ae6-659d580138d5)

## Airflow - 자동화 (자세한 사항은 airflow 폴더 참고)
- 초기에는 DB 업데이트를 함수화하여 구현.
- 이후 Log 데이터 특성을 고려해 처리 속도 저하를 방지해야 한다고 판단해 Airflow 사용.
- 현재 1시간에 한 번씩 실행 중.
