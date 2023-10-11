from jose import JWTError, jwt
from datetime import datetime, timedelta
from server.schemas import token_schemas
from fastapi import Depends, status, HTTPException
from server.models.models import Users, session
from fastapi.security import OAuth2PasswordBearer
import os
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='graphql')
# Seceret key
#Algorithm
# expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            print("id not found")
        token_data = token_schemas.TokenData(id=id)
    except JWTError:
        return "jwtError hy bhai"

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    print("I am token lol please ",token)
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # token = verify_access_token(token, credentials_exception)
    
    # user = session.query(Users).filter(Users.user_id == token.id).first()
    # print(user.user_id)
    return "user"
