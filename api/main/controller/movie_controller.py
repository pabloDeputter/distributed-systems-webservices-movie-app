import requests
import os

from flask_restx import Resource

from ..util.dto import MovieDto
from ..util.decoratorMovies import filter_deleted_movies_func, add_deleted_movie

# Create namespace for controller.
ns = MovieDto.api
# Import models
_movie = MovieDto.movie
_movie_details = MovieDto.movie_details
_cast = MovieDto.cast
_paginated = MovieDto.paginated
_average_scores = MovieDto.average_scores

# Create parser for parsing query parameters.
parser = ns.parser()
# Add page query param.
parser.add_argument(
    "page",
    type=int,
    required=False,
    default=1,
    help="Page number, when larger than total pages the latest page is returned",
    # choices=tuple(range(1, 501)),
)
# Add per_page query param.
parser.add_argument(
    "per_page",
    type=int,
    required=False,
    default=20,
    help="Number of results per page",
)

# Create parser for movie ids
parser_average_scores = ns.parser()
# Add movie_ids param.
parser_average_scores.add_argument(
    'movie_ids',
    type=str,
    required=True,
    help='Movie ids, comma seperated list of movie ids',
    action='split'
)


@ns.route('/<int:movie_id>')
@ns.response(404, 'Movie not found.')
@ns.param('movie_id', 'A movie identifier')
class Movie(Resource):
    @ns.doc('get_movie')
    @ns.marshal_with(_movie_details, code=200)
    def get(self, movie_id):
        """
        Endpoint to retrieve the details of a movie.

        This endpoint retrieves the details of a specific movie identified by `movie_id`, which should be an integer.
        If the movie is found, the endpoint returns the movie's details in JSON format, using the `_movie_details` schema.
        If the movie is not found, a 404 error is returned with a message explaining that the movie was not found.

        :param movie_id: A movie identifier.
        :raises 404: If the movie does not exist.
        :return: A JSON object containing the movie's details.
        """
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US'}

        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}',
            params,
        )
        return filter_deleted_movies_func(response.json()) if response.status_code == 200 else ns.abort(404, f"Movie {movie_id} not found.")

    @ns.doc('delete_movie')
    @ns.response(204, 'Movie successfully deleted')
    def delete(self, movie_id):
        """
        Deletes a specific movie.

        Use this endpoint to delete a specific movie by passing its unique identifier. The deleted movie will be added to
        the list of deleted movies and will not be returned in any subsequent API calls.

        :param movie_id: A movie identifier.
        :return: An empty response with a 204 status code.
                """
        add_deleted_movie(self.get(movie_id))
        return '', 204


@ns.route('/<int:movie_id>/cast')
@ns.response(404, 'Movie not found.')
@ns.param('movie_id', 'A movie identifier')
class MovieCast(Resource):
    @ns.doc('get_movie_cast')
    @ns.marshal_list_with(_cast, envelope='data', code=200)
    def get(self, movie_id):
        """
        Endpoint to retrieve the cast list of a movie.

        This endpoint retrieves the cast list of a specific movie identified by `movie_id`, which should be an integer.

        :param movie_id: A movie identifier.
        :raises 404: If the movie does not exist.
        :return: A JSON object containing the movie's cast.
        """
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US'}

        # Check if given movie id exists
        Movie().get(movie_id)

        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}/credits',
            params,
        )
        return response.json()['cast'] if response.status_code == 200 else ns.abort(404, f"Movie {movie_id} not found.")


@ns.route('/top-movies/<int:amount>')
@ns.param('amount', 'Amount of top movies')
class TopMovies(Resource):
    @ns.doc('get_top_movies')
    @ns.marshal_list_with(_paginated, envelope='data', code=200)
    @ns.expect(parser)
    def get(self, amount):
        """
        Retrieves the top movies from The Movie Database API.

        :param amount: The number of top movies to retrieve.
        :return: A paginated list of popular movies in descending order of popularity.
        """
        # Parse query args.
        global response
        args = parser.parse_args()
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US', 'page': min(args['page'], 500)}

        top_movies: list = []
        while len(top_movies) < amount:
            response = requests.get(
                'https://api.themoviedb.org/3/movie/popular',
                params,
            )
            total_movies: int = response.json()['total_results']
            # Get the number of results per page.
            per_page: int = len(response.json()['results'])
            # Get the number of total pages.
            total_pages: int = min(total_movies // per_page, response.json()['total_pages'])
            # Add to list of movies.
            top_movies += response.json()['results'][:amount - len(top_movies)]
            if params['page'] >= total_pages:
                break
            # Increase page param.
            params['page'] += 1

        # response.json()['results'] = top_movies
        response = response.json()
        response['results'] = top_movies
        return filter_deleted_movies_func(response)


@ns.route('/similar-genre/<int:movie_id>')
@ns.response(404, 'Movie not found.')
@ns.param('movie_id', 'A movie identifier')
class SimilarGenreMovies(Resource):
    @ns.doc('get_similar_genre_movies')
    @ns.marshal_list_with(_paginated, envelope='data', code=200)
    @ns.expect(parser)
    def get(self, movie_id):
        """
        Get a list of movies that have the exact same genres.

        :param movie_id: The identifier of the movie to retrieve the similar genre movies.
        :raises 404: If the movie does not exist.
        :return: A list of movies that share the exact same genres.
        """
        # Parse query args.
        args = parser.parse_args()
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US', 'page': min(args['page'], 500)}

        # Check if given movie id exists
        response = Movie().get(movie_id)

        # Retrieve all genres.
        genres_all: list = requests.get('https://api.themoviedb.org/3/genre/movie/list', {
            'api_key': os.environ.get('THEMOVIEDB_API_KEY'),
            'language': 'en-US'
        }).json()['genres']
        genres_all_ids: list = [d['id'] for d in genres_all]

        # Retrieve details from response
        movie_genres = response['genres']
        movie_genres = [d['id'] for d in movie_genres]

        # Calculate all genres that are not in those of the given movie.
        different_genres = set(genres_all_ids).difference(set(movie_genres))

        # Update params.
        params |= {
            'with_genres': ','.join(str(v) for v in movie_genres),
            'without_genres': ','.join(str(v) for v in different_genres)
        }

        return filter_deleted_movies_func(requests.get(
            'https://api.themoviedb.org/3/discover/movie',
            params
        ).json())


@ns.route('/similar-runtime/<int:movie_id>')
@ns.response(404, 'Movie not found.')
@ns.param('movie_id', 'A movie identifier')
class SimilarRuntimeMovies(Resource):
    @ns.doc('get_similar_runtime_movies')
    @ns.marshal_list_with(_paginated, envelope='data', code=200)
    @ns.expect(parser)
    def get(self, movie_id):
        """
        Get a list of movies that have a similar runtime of +- 10 minutes.

        :param movie_id: The identifier of the movie to retrieve the similar movies.
        :raises 404: If the movie does not exist.
        :return: A list of movies that share a similar runtime.
        """
        # Parse query args.
        args = parser.parse_args()
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US', 'page': min(args['page'], 500)}

        # Check if given movie id exists
        response = Movie().get(movie_id)

        # Update params.
        params |= {
            # Maximum difference of 10 in runtime.
            'with_runtime.lte': response['runtime'] + 10,
            'with_runtime.gte': response['runtime'] - 10
        }

        return filter_deleted_movies_func(requests.get(
            'https://api.themoviedb.org/3/discover/movie',
            params
        ).json())


@ns.route('/overlapping-actors/<int:movie_id>')
@ns.response(404, 'Movie not found.')
@ns.param('movie_id', 'A movie identifier')
class OverlappingActorsMovies(Resource):
    @ns.doc('get_overlapping_actors_movies')
    @ns.marshal_list_with(_paginated, envelope='data', code=200)
    @ns.expect(parser)
    def get(self, movie_id):
        """
        Get a list of movies that share actors with the given movie.

        :param movie_id: The identifier of the movie to retrieve overlapping actors.
        :raises 404: If the movie does not exist.
        :return: A list of movies that share actors with the given movie.
        """
        # Parse query args.
        args = parser.parse_args()
        params = {'api_key': os.environ.get('THEMOVIEDB_API_KEY'), 'language': 'en-US', 'page': min(args['page'], 500)}

        # Retrieve movie cast.
        response = MovieCast().get(movie_id)

        # Update params.
        params |= {
            # Maximum difference of 10 in runtime.
            'with_cast': ','.join(str(v['id']) for v in response['data'][:2]),
        }

        return filter_deleted_movies_func(requests.get(
            'https://api.themoviedb.org/3/discover/movie',
            params
        ).json())


@ns.route('/average-scores')
@ns.response(404, 'Movie not found.')
class AverageScores(Resource):
    @ns.doc('get_average_scores')
    @ns.marshal_with(_average_scores, envelope='data', code=200)
    @ns.expect(parser_average_scores)
    def get(self):
        """
        Endpoint to get the average scores of movies.

        :raises 404: If the movie is not found.
        :return: Returns a dictionary containing a chart and a list of movies with their average scores.
        """
        # Parse query args.
        args = parser_average_scores.parse_args()

        chart_endpoint: str = 'https://quickchart.io/chart/render/zm-cfc18cf3-356e-4c89-b6df-eae582af4a7c'
        movies: list = []

        for movie_id in args['movie_ids']:
            response = Movie().get(movie_id)
            movies.append(response)

        return {
            'chart': f"{chart_endpoint}?data1={','.join(str(v['vote_average']) for v in movies)}&labels={','.join(str(v['title']) for v in movies)}&title=Average Score",
            'movies': movies
        }
