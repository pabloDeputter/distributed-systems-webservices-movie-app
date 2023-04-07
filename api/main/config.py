import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    The base configuration class for the Flask application.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    THEMOVIEDB_API_KEY = os.environ.get('THEMOVIEDB_API_KEY')


class DevelopmentConfig(Config):
    """
    The configuration class for the Flask application when in development mode.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    The configuration class for the Flask application when in production mode.
    """
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
