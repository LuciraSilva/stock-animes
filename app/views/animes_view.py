from app.exceptions.anime_error import AttributeIsMissing, AnimeNotFound, InvalidKey

from app.services import checking_keys, create_animes_table

from flask import Blueprint, request, jsonify

from psycopg2.errors import UndefinedTable, UniqueViolation

from app.models.anime import Anime

bp_animes = Blueprint('animes', __name__, url_prefix='/api')

@bp_animes.route('/animes', methods=('GET', 'POST'))
def get_create():
    if request.method == 'GET':
        try:
            animes = Anime.get_data()
            return jsonify({ 'datas': animes }), 200

        except UndefinedTable:
            return jsonify({ 'datas': [] }), 200

    data = request.json
    
    try:
        checking_keys(data)

        avaliable_data = data

        new_anime = Anime(avaliable_data)

        saved_anime = new_anime.save()

        return saved_anime, 201
    
    except InvalidKey as e:
        return jsonify(e.__dict__), 422

    except AttributeIsMissing as e:

        return {'message': str(e)}, 406

    except UniqueViolation: 
        return {'message': 'Anime already exists'}, 409

    except UndefinedTable:

        create_animes_table()

        try:
            checking_keys(data)

            avaliable_data = data

            new_anime = Anime(avaliable_data)

            saved_anime = new_anime.save()

            return saved_anime, 201

        except InvalidKey as e:
            return jsonify(e.__dict__), 422



@bp_animes.route('/animes/<int:anime_id>', methods=['GET'])
def filter(anime_id: int):
    try:
        getting_data = Anime.get_data_by_id(anime_id)

        return getting_data, 200

    except (UndefinedTable, AnimeNotFound):
        return {}, 404


@bp_animes.route('/animes/<int:anime_id>', methods=['PATCH'])
def update(anime_id: int):
    data = request.json

    try:
        updated_data = Anime.update(anime_id, data)
        return updated_data, 200

    except InvalidKey as e:
        return jsonify(e.__dict__), 422

    except (AnimeNotFound, UndefinedTable):
        return {}, 404


@bp_animes.route('/animes/<int:anime_id>', methods=['DELETE'])
def delete(anime_id: int):
    try:
        Anime.delete(anime_id)
        return '', 204

    except AnimeNotFound as e:
        return {'message': str(e)}, 404

    except UndefinedTable:
        return {}, 404
