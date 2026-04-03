from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from app.routes.auth import auth
    app.register_blueprint(auth)

    with app.app_context():
        from app import models
        db.create_all()

    @app.route('/health')
    def health():
        return {"status": "ok"}

    return app