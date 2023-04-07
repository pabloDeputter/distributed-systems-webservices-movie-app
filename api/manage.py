import os
import sys

from flask_restx import Api
from flask import Blueprint

from main import create_app

from main.controller.movie_controller import ns as movie_ns
from main.controller.auth_controller import ns as auth_ns
from main.controller.account_controller import ns as acc_ns

blueprint = Blueprint('api', __name__)


class MoviesAPI:
    """Class to create and configure the Movies API."""

    def __init__(self):
        """Initialize MoviesAPI instance."""
        self._create_api()

    def _create_api(self):
        """Create API with the path of the Swagger documentation being
        '/docs'. The prefix of the API is '/api', so all API calls must
        be made with the '/api' prefix."""
        self.api = Api(
            blueprint,
            version='1.0',
            title='Movies API',
            description='A simple Movies API',
            doc='/docs',
            prefix='/api',
        )

        # Add namespace to the API
        self.api.add_namespace(movie_ns, path='/movie')
        self.api.add_namespace(auth_ns, path='/authentication')
        self.api.add_namespace(acc_ns, path='/account')

    @staticmethod
    def run():
        """Run the Flask application"""
        mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] and sys.argv[1] in [
            'prod', 'dev'] else 'dev'

        # Create Flask application instance
        app = create_app(mode)

        # Register blueprint with Flask application
        app.register_blueprint(blueprint)

        # Push app context
        app.app_context().push()

        # Get port number from environment variables or use default 5000
        port = int(os.environ.get("PORT", 5000))

        # Run the Flask application
        app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    # Create an instance of MoviesAPI and run the Flask application
    api = MoviesAPI()
    api.run()
