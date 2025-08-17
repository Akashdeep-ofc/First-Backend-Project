from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import select
from typing import Annotated
from ..database import SessionDep
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(session:SessionDep, vote:schemas.Vote,
        user:Annotated[schemas.UserPublic,Depends(oauth2.get_current_user)]):
    # checking if that post exists
    post_id = session.get(models.Post,vote.post_id)
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist")
    # print("ran here", vote)

    voted_row = session.get(models.Votes,(user.id,vote.post_id))
    if vote.dir:
        if voted_row:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Already Liked this Post")
        else:
            new_vote = schemas.VoteCreate(user_id=user.id,post_id=vote.post_id)
            db_vote = models.Votes.model_validate(new_vote)
            session.add(db_vote)
            session.commit()
            session.refresh(db_vote)
            return db_vote
    else:
        if not voted_row:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Already Not Liked this Post")
        else:
            session.delete(voted_row)
            session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

