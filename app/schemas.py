from sqlmodel import SQLModel
from datetime import datetime
from pydantic import EmailStr



# Post Info Related
class PostBase(SQLModel):
    title:str
    content:str
    published:bool

class PostPublic(PostBase):
    id:int
    owners_id:int|None
    # created_at:datetime
    pass

class PostCreate(PostBase):
    owners_id:int|None
    pass

class PostUpdate(SQLModel):
    title:str|None = None
    content:str|None = None
    published:bool|None = None

class sub_step(PostPublic):
    created_at:datetime


class PostVotesCount(SQLModel):
    Post:sub_step
    votes:int


# User Info Related

class UserBase(SQLModel):
    email:EmailStr

class UserCreate(UserBase):
    password:str

class UserPublic(UserBase):
    id:int
    
class UserLogin(UserCreate):
    pass




# Token Related
class Token(SQLModel):
    access_token:str
    token_type:str
    pass

class TokenData(SQLModel):
    id:int
    pass



# Voting
class Vote(SQLModel):
    post_id:int
    dir:bool

class VoteCreate(SQLModel):
    user_id:int
    post_id:int