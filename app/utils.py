from fastapi import status, HTTPException
from passlib.context import CryptContext
from . import models, schemas
from sqlmodel import select
from .database import SessionDep

pwd_content = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

def email_verify(user:schemas.UserBase,session:SessionDep):
    existing_user = session.exec(select(models.User).where(models.User.email==user.email)).first()
    print(existing_user)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Sorry this user already exists")
    
def hash_this(password:str):
    return pwd_content.hash(password)

def verify(ideal_password:str,input_password:str):
    return pwd_content.verify(ideal_password,input_password)