from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api.v1.users import users_bp
    from app.api.v1.amenities import amenities_bp
    from app.api.v1.places import places_bp
    from app.api.v1.reviews import reviews_bp
    from app.api.v1.auth import auth_bp

    app.register_blueprint(users_bp,     url_prefix='/api/v1/users')
    app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')
    app.register_blueprint(places_bp,    url_prefix='/api/v1/places')
    app.register_blueprint(reviews_bp,   url_prefix='/api/v1/reviews')
    app.register_blueprint(auth_bp,      url_prefix='/api/v1/auth')

    with app.app_context():
        db.create_all()

    return app
