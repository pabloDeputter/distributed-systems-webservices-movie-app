import requests
import os

from flask import request
from flask_restx import Resource

from ..util.dto import AuthDto

# Create namespace for controller.
ns = AuthDto.api
# Import models
_token = AuthDto.token
_session = AuthDto.session
_request_token = AuthDto.request_token
_session_id = AuthDto.session_id


@ns.route('/token/new')
@ns.response(404, "Resource was not found.")
class NewToken(Resource):
    @ns.doc('get_new_token')
    @ns.marshal_with(_token, envelope='data', code=200)
    def get(self):
        """
        Endpoint for creating a new authentication token from The Movie DB.

        Generates a new authentication token to be used to authenticate the user in subsequent requests to The Movie Database API.

        :return: A JSON object containing the newly created authentication token.
        :raise 404: If the request was unsuccessful.
        """
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US'}

        response = requests.get(
            'https://api.themoviedb.org/3/authentication/token/new', params
        )
        return (
            response.json()
            if response.status_code == 200
            else ns.abort(404, "Resource was not found")
        )


@ns.route('/session')
@ns.response(404, "Resource was not found.")
class NewSession(Resource):
    @ns.doc('post_session')
    @ns.marshal_with(_session, envelope='data', code=200)
    @ns.expect(_request_token, validate=True)
    def post(self):
        """
        Creates a new session with The Movie DB.

        Creates a new user session based on a request token, which was previously generated and authenticated
        by the user through the TMDB.

        :return: A JSON object containing the newly created session.
        :raise 404: If the request was unsuccessful.
        """
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US'}

        response = requests.post(
            url='https://api.themoviedb.org/3/authentication/session/new', params=params, data=request.json)

        return (
            response.json()
            if response.status_code == 200
            else ns.abort(404, "Resource was not found")
        )

    @ns.doc('delete_session')
    @ns.response(200, 'Session successfully deleted')
    @ns.expect(_session_id, validate=True)
    def delete(self):
        """
        Deletes the current session with The Movie DB.

        Deletes the current user session, effectively logging the user out of the TMDB.

        :return: A JSON object containing the status of the deletion request.
        :raise 404: If the request was unsuccessful.
        """
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US'}

        response = requests.delete(
            url='https://api.themoviedb.org/3/authentication/session', params=params, data=request.json)

        return (
            response.json()
            if response.status_code == 200
            else ns.abort(404, "Resource was not found")
        )
