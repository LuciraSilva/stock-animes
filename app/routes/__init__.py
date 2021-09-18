from flask import Blueprint
from . import animes_blueprint

bp = Blueprint('bp_api', __name__, url_prefix='/api')

bp.register_blueprint(animes_blueprint.bp)
