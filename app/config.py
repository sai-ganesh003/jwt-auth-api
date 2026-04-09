import os
from dotenv import load_dotenv

load_dotenv(override=False)

DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'mysql+pymysql://root:tKSPOAOhzBHZVoNVuYQkEXwrwLHpppdE@maglev.proxy.rlwy.net:44739/railway'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 900
    JWT_REFRESH_TOKEN_EXPIRES = 604800