from app.exceptions.animes_exceptions import AttributeIsMissingError, AnimeNotFoundError, InvalidKeyError
from psycopg2.errors import UndefinedTable, UniqueViolation
from app.services import create_animes_table
from psycopg2 import OperationalError
from flask import request, jsonify
from app.models.animes_model import Anime


def get_animes():

    try:
        animes = Anime.get_data()
        return jsonify({ 'datas': animes }), 200

    except UndefinedTable:

        return {}, 404

    except OperationalError:

        return {}, 404


def create_anime():

    data = request.json
    
    try:

        new_anime = Anime(data)

        saved_anime = new_anime.create()

        return saved_anime, 201

    except InvalidKeyError as e:
        return jsonify(e.__dict__), 422

    except AttributeIsMissingError as e:

        return {'message': str(e)}, 406

    except UniqueViolation: 
        return {'message': 'Anime already exists'}, 409

    except OperationalError:
        
        return {}, 404

    except UndefinedTable:

        create_animes_table()

        try:

            new_anime = Anime(data)

            saved_anime = new_anime.create()

            return saved_anime, 201

        except InvalidKeyError as e:
            return jsonify(e.__dict__), 422


def get_anime_by_id(anime_id: int):
    try:
        getting_data = Anime.get_data_by_id(anime_id)

        return getting_data, 200

    except AnimeNotFoundError as e:
        return {'message': str(e)}, 404

    except (UndefinedTable, OperationalError):
        return {}, 404


def update_anime_data(anime_id: int):
    data = request.json

    try:
        updated_data = Anime.update(anime_id, data)
        return updated_data, 200

    except InvalidKeyError as e:
        return jsonify(e.__dict__), 422

    except AnimeNotFoundError as e:
        return {'message': str(e)}, 404

    except (UndefinedTable, OperationalError):
        return {}, 404


def delete_anime(anime_id: int):
    try:
        Anime.delete(anime_id)
        return '', 204

    except AnimeNotFoundError as e:
        return {'message': str(e)}, 404

    except (UndefinedTable, OperationalError):
        return {}, 404
