from datetime import datetime, timedelta

import jwt
import bcrypt
import uuid
import logging

from src.config import settings




def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))

def create_access_token(user_data,expiry:timedelta=timedelta(hours=1)):

    payloadd={}
    payloadd['user']=user_data
    payloadd['exp']=datetime.now()+expiry
    payloadd['jti'] = str(uuid.uuid4())

    token=jwt.encode(
        payload=payloadd,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_token(token):
    try:
        token_data=jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
