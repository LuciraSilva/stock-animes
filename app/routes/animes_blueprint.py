from app.controllers.animes_controller import create_anime, delete_anime, get_anime_by_id, get_animes, update_anime_data
from flask import Blueprint

bp = Blueprint('bp_animes', __name__, url_prefix='/animes')


bp.post('')(create_anime)

bp.get('')(get_animes)

bp.get('/<int:anime_id>')(get_anime_by_id)


bp.patch('/<int:anime_id>')(update_anime_data)

bp.delete('/<int:anime_id>')(delete_anime)
