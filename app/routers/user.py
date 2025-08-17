from .. import models, schemas, utils
from ..database import SessionDep
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException, APIRouter

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/",response_model=schemas.UserPublic)
def create_user(session:SessionDep,user:schemas.UserCreate):

    user.password = utils.hash_this(user.password)
    utils.email_verify(user,session)
    # print(f"Inside user, password :f{user.password}, email :f{user.email}")
    new_user = models.User.model_validate(user)
    session.add(new_user)
    # Adding this block in case multiple Requests come and pass through earlier function
    try:
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already registered."
        )
    # session.commit()
    # session.refresh(new_user)
    # return new_user

@router.get("/{id}",response_model=schemas.UserPublic)
def user_id(session:SessionDep,id:int):
    user = session.get(models.User,id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sorry bro, no ID like {id} exists")
    return user
