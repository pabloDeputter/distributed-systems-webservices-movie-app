from flask import Flask
from flask_cors import CORS

from .config import config_by_name


def create_app(config_name: str) -> Flask:
    """
    Factory function that creates a new Flask application instance with the given configuration.

    :param config_name: The name of the configuration to use.
    :type config_name: str
    :return: A new Flask application instance.
    """
    app = Flask(__name__, static_folder='../../build', static_url_path='/')
    # configure the application using the specified configuration
    app.config.from_object(config_by_name[config_name])
    # enable CORS support for the application
    cors = CORS(app, origins=["*"], supports_credentials=True)
    return app
