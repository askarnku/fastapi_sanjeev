from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from decouple import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorythm
# Expiration

SECRET_KEY = config("SECRET_KEY")
ALGORYTHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)


def create_access_token(data: dict):
    # User sent data which will be encoded
    to_encode = data.copy()

    # time that token expires (takes current time and adds delta time which is now + 30 min)
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # we are adding key-value {exp : 19329382} which is time when token expires
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
        print(payload)
        parm_id: str = str(payload.get("user_id"))
        if not parm_id:
            raise credentials_exceptions
        token_data = schema.TokenData(id=parm_id)
    except JWTError:
        raise credentials_exceptions

    print(token_data)
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW_Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
