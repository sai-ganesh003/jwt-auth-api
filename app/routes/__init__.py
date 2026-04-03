from flask import Flask
from app.routes.auth import auth

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth)

    @app.route('/health')
    def health():
        return {"status": "ok"}

    return app