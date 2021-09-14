from flask import Flask

def init_app(app: Flask):
    from app.views.animes_view import bp_animes
    app.register_blueprint(bp_animes)
    
    return app