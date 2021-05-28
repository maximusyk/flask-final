import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "flask_course.db")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # SQLALCHEMY_DATABASE_URI = "postgres://cnpqfsqalnyejt:e5a01a10b9801790485abcdd19d1a9d4e49b37af80ffb7fbbb7d6f13ff0866f5@ec2-54-220-170-192.eu-west-1.compute.amazonaws.com:5432/d9vus48e5c6hqn"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
