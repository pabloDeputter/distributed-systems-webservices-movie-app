import requests
import os

from flask import request
from flask_restx import Resource

from ..util.dto import AccountDto
from ..util.dto import MovieDto
from ..util.decoratorMovies import filter_deleted_movies_func

# Create namespace for controller.
ns = AccountDto.api
# Import models
_account = AccountDto.account
_fav_body = AccountDto.fav_body
_fav_response = AccountDto.fav_response
_movie = MovieDto.movie
_paginated = MovieDto.paginated

# Create parser for parsing query parameters.
parser = ns.parser()
# Add page query param.
parser.add_argument(
    "session_id",
    type=str,
    required=True,
    help="Session_id, required for account related operations.",
)


@ns.route('/')
@ns.response(401, "Authentication failed, no permission to this service.")
@ns.response(404, "Resource was not found.")
class Account(Resource):
    @ns.doc('get_account')
    @ns.marshal_with(_account, envelope='data', code=200)
    @ns.expect(parser, validate=True)
    def get(self):
        """
        Account resource endpoint for retrieving account information.

        :return: Returns account information in JSON format.
        :raise 401: Authentication failed, no permission to this service.
        :raise 404: Resource was not found.
        """
        # Parse query args.
        args = parser.parse_args()
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'session_id': args['session_id'],
                  'language': 'en-US'}

        response = requests.get(
            url='https://api.themoviedb.org/3/account', params=params
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return ns.abort(401, response.json()['status_message'])
        elif response.status_code == 404:
            return ns.abort(404, response.json()['status_message'])
        else:
            return ns.abort(404, "Resource was not found")


@ns.route('/<int:account_id>/favorite')
@ns.response(401, "Authentication failed, no permission to this service.")
@ns.response(404, "Resource was not found.")
class AccountFavorite(Resource):
    @ns.doc('post_account_favorite')
    @ns.marshal_with(_fav_response, envelope='data', code=200)
    @ns.expect(_fav_body, parser, validate=True)
    def post(self, account_id):
        """
        Add a movie or TV show to the user's favorites list.

        :param account_id: The account ID of the user.
        :return: The response data, which contains the movie or TV show that was added to the user's favorites list.
        :raises 401: If authentication failed, indicating no permission to this service.
        :raises 404: If the specified resource was not found.
        """
        # Parse query args.
        args = parser.parse_args()
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'session_id': args['session_id'],
                  'language': 'en-US'}

        response = requests.post(
            url=f'https://api.themoviedb.org/3/account/{account_id}/favorite', params=params, json=request.json,
        )

        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 401:
            return ns.abort(401, response.json()['status_message'])
        elif response.status_code == 404:
            return ns.abort(404, response.json()['status_message'])
        else:
            return ns.abort(404, "Resource was not found")


@ns.route('/<int:account_id>/favorite/movies')
@ns.response(401, "Authentication failed, no permission to this service.")
@ns.response(404, "Resource was not found.")
class AccountFavoriteMovies(Resource):
    @ns.doc('get_account_favorite_movies')
    @ns.marshal_with(_paginated, envelope='data', code=200)
    @ns.expect(parser, validate=True)
    def get(self, account_id):
        """
        Retrieve a paginated list of the current user's favorite movies.

        :param account_id: An integer representing the id of the user account.
        :raises 401: If the authentication fails or if there is no permission to access the service.
        :raises 404: If the resource was not found.
        :return: A paginated response containing the user's favorite movies.
        """
        # Parse query args.
        args = parser.parse_args()
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'session_id': args['session_id'],
                  'language': 'en-US'}

        response = requests.get(
            url=f'https://api.themoviedb.org/3/account/{account_id}/favorite/movies', params=params
        )

        if response.status_code == 200:
            return filter_deleted_movies_func(response.json())
        elif response.status_code == 401:
            return ns.abort(401, response.json()['status_message'])
        elif response.status_code == 404:
            return ns.abort(404, response.json()['status_message'])
        else:
            return ns.abort(404, "Resource was not found")