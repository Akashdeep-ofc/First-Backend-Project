
from fastapi import FastAPI, Response, status, HTTPException, Depends, Query
from fastapi.params import Body
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from . import models, schemas, utils
from .database import SessionDep,create_database
from .routers import auth, post,user,vote

# Starting FastAPI app
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.on_event("startup")
def on_startup():
    create_database()



# All routes and their logics
## Sample base Route function
@app.get("/")
async def root():
    return {"message": "Hello Biyaatch"}

