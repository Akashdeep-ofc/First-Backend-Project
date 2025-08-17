from .. import models, schemas
from ..oauth2 import get_current_user
from ..database import SessionDep
from fastapi import status, HTTPException, Query, Response, APIRouter, Depends
from typing import Annotated
from sqlmodel import select, func, asc
# from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


## get all posts from dataset
@router.get("/", response_model=list[schemas.PostVotesCount])
# @router.get("/")
def get_post(session:SessionDep,current_user:Annotated[schemas.UserPublic,Depends(get_current_user)],
            search:str="",off:int = 0, lim:Annotated[int,Query(le=50)]=50):
    # result = session.exec(select(models.Post).where(models.Post.title.ilike(f"%{search}%")).offset(off).limit(lim)).all()

    query = session.exec(select(models.Post, func.count(models.Votes.post_id).
                                label("votes")).
                                join(models.Votes, models.Votes.post_id == models.Post.id,isouter=True).
                                group_by(models.Post.id).
                                where(models.Post.title.ilike(f"%{search}%")).
                                offset(off).limit(lim).
                                order_by(asc(models.Post.id))).all()
    # result = [dict({"Post":i,"Votes":j}) for i, j in query]
    # schemas.PostVotesCount()

    return query
    # return query



## Getting post by ID
@router.get("/{id}", response_model=schemas.PostPublic)
def get_post_id(id:int,session:SessionDep,
                current_user:Annotated[schemas.UserPublic,Depends(get_current_user)]):
    result = session.get(models.Post,id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID = {id} was not found")
    return result



## Creating a Post
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostPublic)
def create_post(post:schemas.PostCreate,session:SessionDep,
                current_user:Annotated[schemas.UserPublic,Depends(get_current_user)]):
    print(current_user.email)
    post.owners_id=current_user.id
    db_post = models.Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post



## Updating a Post
@router.put("/{id}",response_model=schemas.PostPublic)
def update_post(id:int,post:schemas.PostUpdate,session:SessionDep,
                current_user:Annotated[schemas.UserPublic,Depends(get_current_user)]):
    
    original_post = session.get(models.Post,id)
    if not original_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sorry Babu, ID no. {id} yahan nhi hai")
    if not original_post.owners_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Pakad liya saale ko, yeh ID teri nhi hai kutte")
    changes_dict = post.model_dump(exclude_unset=True)
    original_post.sqlmodel_update(changes_dict)
    session.add(original_post)
    session.commit()
    session.refresh(original_post)
    return original_post


## Deleting a Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_id(id:int,session:SessionDep,
                   current_user:Annotated[schemas.UserPublic,Depends(get_current_user)]):
    post = session.get(models.Post,id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with ID={id} does not exist, Sorry ....")
    if not post.owners_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Pakad liya saale ko, yeh ID teri nhi hai kutte")
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
