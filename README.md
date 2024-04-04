# Multi Recipe Project
- Project 기간 : 2023-12-01 ~ 2024-01-04
- 프로젝트 목표 : 이미지를 익숙하게 여기는 2030대를 타겟으로 하는 레시피 사이트를 만들자!
- 프로젝트 참가자 및 담당 업무
    - 이서연 : 팀장/크롤링/데이터 분석/CNN, 취향테스트기반 추천, FastText모델링 및 모듈화/Airflow 파이프라인 구현/보고서
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