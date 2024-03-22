from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from schemas import Post, PostBase, UserCreate, UserOut
import uuid
from icecream import ic
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from decouple import config
import models
from database import engine, get_db
from typing import List
import utils
from routers import users, posts, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="fastapi",
        user="postgres",
        port=5432,
        password=config("DB_PASSWORD"),
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Database connection was successfull")

except Exception as ex:
    raise Exception(ex)

my_posts = [
    {
        "title": "Nike Pegasus 40",
        "content": "A advance generation shoe for running",
        "published": True,
        "rating": 5,
        "id": "bf50381a-9e8c-4b3c-9f66-259192ff424a",
    },
    {
        "title": "Nike Pegasus 39",
        "content": "A cool looking shoe for running",
        "published": True,
        "rating": 5,
        "id": "f2615b82-f2ff-4003-96f0-ef05eca94ce6",
    },
    {
        "title": "Nike Pegasus 39",
        "content": "A cool looking shoe for running",
        "published": True,
        "rating": 5,
        "id": 123,
    },
]


def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}  # FastAPI directly converts this into JSON



app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
