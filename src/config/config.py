import os

from flask import Config


class BaseConfig(Config):
    pass


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///local.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")
    # UPLOAD_FOLDER = str(Path(basedir, "src", "uploads"))


config = {
    "development": DevelopmentConfig,
}
