from fastapi import APIRouter, HTTPException,status, Depends
from sqlmodel import select
from ..database import SessionDep
from .. import models, schemas, utils
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/", response_model=schemas.Token)
def login(session:SessionDep, cred:OAuth2PasswordRequestForm = Depends()):
    email =cred.username
    password = cred.password
    # print(email)
    # print(password)
    user = session.exec(select(models.User).where(models.User.email==email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Invalid Cred")
    if not utils.verify(password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Invalid Cred")
    JWToken = create_access_token(data={"user_id":user.id})
    return {"access_token":JWToken, "token_type":"bearer"}
    
