from typing import Annotated
from fastapi import Depends, status,HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,models
from .database import SessionDep
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    token = data.copy()
    exp_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token.update({"exp":exp_time})
    encoded_jwt = jwt.encode(token,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    
    except JWTError:
        raise credentials_exception
    


def get_current_user(token:Annotated[str,Depends(oauth2_scheme)], session:SessionDep):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    verified = verify_access_token(token,credentials_exception)
    user = session.exec(select(models.User).where(models.User.id==verified.id)).first()
    if not user:
        raise credentials_exception
    return user