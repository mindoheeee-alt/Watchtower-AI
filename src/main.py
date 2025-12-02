from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from src.config.config import config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # TODO: 미로그인 상태로 접근제한 페이지에 접속시 리다이렉트 할 엔드포인트
login_manager.login_message = ""


def create_app(env: str = "development"):
    app = Flask(__name__)

    if env in config:
        app.config.from_object(config[env])
    else:
        raise KeyError(f"Environment {env} not found.")

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from src.root.views import root_views
    from src.user.views import user_views
    from src.auth.views import auth_views

    app.register_blueprint(root_views, url_prefix="/")
    app.register_blueprint(user_views, url_prefix="/user")
    app.register_blueprint(auth_views, url_prefix="/auth")

    return app
