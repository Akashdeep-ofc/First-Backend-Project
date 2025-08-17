from sqlalchemy import Column, Boolean, text, DateTime
from sqlmodel import SQLModel,Field, ForeignKey, Relationship
from datetime import datetime
from typing import Optional


class User(SQLModel,table=True):
    __tablename__="users"
    id:int|None=Field(default=None, primary_key=True, nullable=False)
    email:str=Field(nullable=False, unique=True)
    password:str=Field(nullable=False)
    created_at:datetime|None=Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False),
            default=None
    )
    posts:list["Post"] = Relationship(back_populates="owner")





class Post(SQLModel,table=True):
    __tablename__= "posts"

    id:int|None=Field(default=None,primary_key=True,nullable=False)
    title:str = Field(index=True,nullable=False)
    content:str = Field(nullable=False)
    published: bool = Field(
        sa_column=Column(Boolean, server_default="True", nullable=False)
    )
    created_at:datetime|None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False),
            default=None
    )
    owners_id:int|None=Field(
        sa_column=Column(
            ForeignKey(
                "users.id",
                ondelete="CASCADE",
                onupdate="CASCADE"
            ),
            nullable=False
        )
    )
    owner:Optional[User]=Relationship(back_populates="posts")




class Votes(SQLModel, table=True):
    __tablename__="votes"
    user_id:int = Field(
        sa_column=(
            Column(
                ForeignKey(
                    "users.id",
                    ondelete="CASCADE"
                ),
                primary_key=True,
                nullable=False,

            )
        ))
    post_id:int = Field(
        sa_column=(
            Column(
                ForeignKey(
                    "posts.id",
                    ondelete="CASCADE"
                ),
                primary_key=True,
                nullable=False,

            )
        ))