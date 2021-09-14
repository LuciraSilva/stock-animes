from app.services import create_animes_table, create_db
from app import views
from flask import Flask

def create_app():
    app = Flask(__name__)

    create_db()
    
    create_animes_table()

    views.init_app(app)
    
    return app