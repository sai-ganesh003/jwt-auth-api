class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:root009@localhost:3306/jwt_auth_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False