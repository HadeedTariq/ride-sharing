from django.conf import settings

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def generate_refresh_access_token(user):

    access_payload = {
        "username": user.username,  # Issued at time
        "email": user.email,
        "id": user.id,  # Issued at time
    }
    refresh_payload = {"id": user.id}

    access_token = jwt.encode(
        access_payload,
        settings.JWT_ACCESS_TOKEN_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    refresh_token = jwt.encode(
        refresh_payload,
        settings.JWT_REFRESH_TOKEN_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return {"refresh_token": refresh_token, "access_token": access_token}


def validate_access_token(token):
    try:
        user = jwt.decode(
            token,
            settings.JWT_ACCESS_TOKEN_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return user
    except ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except InvalidTokenError:
        raise ValueError("Invalid token.")


def validate_refresh_token(token):
    try:
        user = jwt.decode(
            token,
            settings.JWT_REFRESH_TOKEN_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return user["username"]
    except ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except InvalidTokenError:
        raise ValueError("Invalid token.")
