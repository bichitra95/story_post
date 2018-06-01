from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bichitra95@localhost:5432'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from apis.models import db
    db.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from apis.views import stories
    app.register_blueprint(stories)