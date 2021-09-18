from app import routes
from app.services import create_animes_table, create_db
from flask import Flask

app = Flask(__name__)

app.register_blueprint(routes.bp)

create_db()

create_animes_table()

