from flask import Flask, jsonify
import os
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv

from src.routes.auth import auth_bp
from src.routes.posts import posts_bp
from src.database import db
from src.config.swagger import template, swagger_config
from src.constants.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# resources - https://flask.palletsprojects.com/en/stable/tutorial/factory/


def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            # JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=7),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            Swagger={"title": "Blog API", "uiversion": 3},
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    Swagger(app, config=swagger_config, template=template)

    @app.get("/")
    def health_check():
        return jsonify({"message": "It's working"})
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def page_not_found(error):
        return jsonify({"error": "Not found"}), HTTP_404_NOT_FOUND

    # The server_error() only works when debug mode is off or when in production
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def server_error(error):
        return (
            jsonify({"error": "Something went wrong. Try again later."}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
