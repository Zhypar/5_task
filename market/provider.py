import datetime
import jwt
from eshop.settings import REFRESH_TOKEN_SECRET
from decouple import config


def generate_access_token(user):
    access_token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "iat": datetime.datetime.utcnow(),
    }

    access_token = jwt.encode(
        access_token_payload, config("SECRET_KEY"), algorithm="HS256"
    ).decode("utf-8")

    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }

    refresh_token = jwt.encode(
        refresh_token_payload, REFRESH_TOKEN_SECRET, algorithm="HS256"
    ).decode("utf-8")

    return refresh_token
