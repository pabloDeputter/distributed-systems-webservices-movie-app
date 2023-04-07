from flask_restx import Namespace, fields


class MovieDto:
    api = Namespace('Movie', description='Movie related operations.')
    # Full movie model
    movie = api.model('movie', {
        'adult': fields.Boolean(),
        'backdrop_path': fields.String(),
        'genre_ids': fields.List(fields.Integer()),
        'id': fields.Integer(required=True),
        "original_language": fields.String(),
        "original_title": fields.String(),
        "overview": fields.String(),
        "popularity": fields.Float(),
        "poster_path": fields.String(),
        "release_date": fields.String(),
        "title": fields.String(),
        "video": fields.Boolean(),
        "vote_average": fields.Float(),
        "vote_count": fields.Integer(),
    })

    # TODO - expand...?
    movie_details = api.model('movie_details', {
        'adult': fields.Boolean(),
        'backdrop_path': fields.String(),
        'budget': fields.Integer(),
        'genres': fields.List(fields.Nested(api.model('genre', {
            'id': fields.Integer(),
            'name': fields.String()
        }))),
        'id': fields.Integer(required=True),
        'imdb_id': fields.String(),
        "original_language": fields.String(),
        "original_title": fields.String(),
        "overview": fields.String(),
        "popularity": fields.Float(),
        "poster_path": fields.String(),
        "release_date": fields.String(),
        "title": fields.String(),
        "video": fields.Boolean(),
        "vote_average": fields.Float(),
        "vote_count": fields.Integer(),
        'runtime': fields.Integer(),
    })

    cast = api.model('cast', {
        'adult': fields.Boolean(),
        'gender': fields.Integer(),
        'id': fields.Integer(),
        'known_for_department': fields.String(),
        'name': fields.String(),
        'original_name': fields.String(),
        'popularity': fields.Integer(),
        'profile_path': fields.String(),
        'cast_id': fields.Integer(),
        'character': fields.String(),
        'credit_id': fields.String(),
        'order': fields.Integer(),
    })

    paginated = api.model('paginated', {
        'page': fields.Integer(),
        'results': fields.List(fields.Nested(movie)),
        'total_results': fields.Integer(),
        'total_pages': fields.Integer()
    })

    average_scores = api.model('average_scores', {
        'chart': fields.String(),
        'movies': fields.List(fields.Nested(movie_details))
    })


class AuthDto:
    api = Namespace('Authentication', description='Authentication related operations.')

    token = api.model('token', {
        'success': fields.Boolean(),
        'expires_at': fields.String(),
        'request_token': fields.String()
    })

    request_token = api.model('request_token', {
        'request_token': fields.String()
    })

    session_id = api.model('session_id', {
        'session_id': fields.String()
    })

    session = api.model('session', {
        'success': fields.Boolean(),
        'session_id': fields.String()
    })


class AccountDto:
    api = Namespace('Account', description='Account related operations.')

    account = api.model('account', {
        "avatar": fields.Nested(api.model('avatar', {
            'gravatar': fields.Nested(api.model('gravatar', {
                'hash': fields.String()
            }))
        })),
        "id": fields.Integer(),
        "iso_639_1": fields.String(),
        "iso_3166_1": fields.String(),
        "name": fields.String(),
        "include_adult": fields.Boolean(),
        "username": fields.String(),
    })

    fav_body = api.model('fav_body', {
        'media_type': fields.String(),
        'media_id': fields.Integer(),
        'favorite': fields.Boolean()

    })

    fav_response = api.model('fav_response', {
        'success': fields.Boolean(),
        'status_code': fields.Integer(),
        'status_message': fields.String()
    })
