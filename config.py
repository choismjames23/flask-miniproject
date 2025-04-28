import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )# DB 연결
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 데이터 변경 사항 추척 기능 비활성화 (메모리 사용량 절약)
    SQLALCHEMY_POOL_SIZE = 10 # 동시 연결 가능한 최대 커넥션 개수
    SQLALCHEMY_POOL_TIMEOUT = 5 # 5초 내에 DB 연결 실패 시 오류 발생
    SQLALCHEMY_POOL_RECYCLE = 1800 # 1800초(30분)동안 유지된 커넥션을 자동으로 닫힘
    SQLALCHEMY_MAX_OVERFLOW = 5 # 커넥션 풀이 가득 찼을 때, 추가로 허용할 수 있는 연결 개수
    SQLALCHEMY_ECHO = False # SQL 실행 로그 미출력
    reload = True # 서버를 자동으로 리로드

    API_TITLE = 'My API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"