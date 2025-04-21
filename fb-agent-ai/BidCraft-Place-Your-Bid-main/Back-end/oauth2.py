from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException,status
import schemas
import database
import models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# import config

# oauthScheme = OAuth2PasswordBearer(tokenUrl="login")
# SECRET_KEY = config.Settings.secret_key
# ALGORITHM = config.Settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = config.Settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24*60

BLACKLISTED_TOKENS = set()

def blacklist_token(token: str):
    BLACKLISTED_TOKENS.add(token)

def createAccessToken(data: dict):

    toEncode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    toEncode.update({"exp": expire})

    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT


def verifyAccessToken(Token: str, credentialException):

    try:
        payload = jwt.decode(Token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentialException
        tokenData = schemas.TokenData(user_id=user_id)
    except JWTError as e:
        print(e)
        raise credentialException

    return tokenData


def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentialException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Token is invalid",
                                        headers={"WWW-Authenticate": "Bearer"})

    token = verifyAccessToken(token, credentialException)
    user = db.query(models.User).filter(
        models.User.user_id == token.user_id).first()
    return user