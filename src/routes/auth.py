from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flasgger import swag_from
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED,
)
from src.database import User, db

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.post("/register")
@swag_from('../docs/auth/register.yaml')
def register():
    email = request.json["email"]
    password = request.json["password"]

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email is taken"}), HTTP_409_CONFLICT

    if len(password) < 6:
        return (
            jsonify({"error": "Password should be graeter than 6"}),
            HTTP_400_BAD_REQUEST,
        )

    pwd_hash = generate_password_hash(password)

    user = User(email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify({"message": "User created", "user": {"email": email}}),
        HTTP_201_CREATED,
    )


@auth_bp.post("/login")
@swag_from('../docs/auth/login.yaml')
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.password, password):
            user_id = str(user.id)
            refresh = create_refresh_token(identity=user_id)
            access = create_access_token(identity=user_id)

            return (
                jsonify(
                    {
                        "user": {
                            "refresh": refresh,
                            "access": access,
                            "username": user.username,
                            "email": user.email,
                        }
                    }
                ),
                HTTP_200_OK,
            )

    return jsonify({"error": "Wrong credentials"}), HTTP_401_UNAUTHORIZED


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return (
        jsonify(
            {
                "username": user.username,
                "email": user.email,
            }
        ),
        HTTP_200_OK,
    )


@auth_bp.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_users_token():
    user_id = get_jwt_identity()
    access = create_access_token(user_id)

    return jsonify({"access": access}), HTTP_200_OK
