from ..util.dto import MovieDto

from typing import Dict, List

#  A dictionary containing deleted movies. The keys are the movie IDs and the values are
#  dictionaries containing movie details.
deletedMovies: Dict[int, dict] = {}


def add_deleted_movie(data: dict):
    """
    Add a deleted movie to the `deletedMovies` dictionary.

    :param data: A dictionary containing movie details, including the ID of the movie.
    """
    deletedMovies.update({data['id']: data})


def get_deleted_movies_ids() -> List:
    """
    Get a list of IDs for all deleted movies.

    :return: A list of IDs for all deleted movies.
    """
    return list(deletedMovies.keys())


def filter_deleted_movies(func):
    """
    A decorator that filters out deleted movies from the result of a function.

    :param func: The function to decorate.
    :return: The decorated function.
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # If return type is a list, filter out the deleted movies.
        if isinstance(result, list):
            result = [movie for movie in result if movie['id'] not in deletedMovies]
        # If return type is a dict and is a deleted movie, abort and return 404
        elif isinstance(result, dict) and 'id' in result:
            if result['id'] in deletedMovies:
                return MovieDto.api.abort(404, f"Movie {result['id']} not found.")
        elif isinstance(result, dict) and 'data' in result:
            result['data']['results'] = [movie for movie in result['data']['results'] if
                                         movie['id'] not in deletedMovies]
        return result

    return wrapper


def filter_deleted_movies_func(result: object) -> object:
    """
    A normal function that filters out deleted movies since the swagger doesn't include documentation
    when custom decorator is used on top of endpoint.

    :param result: The unfiltered movies
    :return: The filtered movies
    """
    # If return type is a list, filter out the deleted movies.
    if isinstance(result, list):
        result = [movie for movie in result if movie['id'] not in deletedMovies]
    # If return type is a dict and is a deleted movie, abort and return 404
    elif isinstance(result, dict) and 'id' in result:
        if result['id'] in deletedMovies:
            return MovieDto.api.abort(404, f"Movie {result['id']} not found.")
    elif isinstance(result, dict) and 'page' in result:
        result['results'] = [movie for movie in result['results'] if
                                     movie['id'] not in deletedMovies]
    return result
