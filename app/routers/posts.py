from fastapi import  Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from schemas import Post, PostBase
import uuid
from icecream import ic
# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from decouple import config
import models
from database import get_db
from typing import List
import utils
import oauth

router = APIRouter( prefix= "/posts", tags=["Posts"])


# we can use List from typing library and we can also use list[Post] from python directly
# Reference: https://fastapi.tiangolo.com/tutorial/response-model/#response_model-parameter
@router.get("/", response_model=List[Post])
async def get_posts(db: Session = Depends(get_db), user_id = Depends(oauth.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # return  posts  # FastAPI directly converts this into JSON
    return posts


# create post
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Post,
    response_model_exclude=["title", "content"],
)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(post: PostBase, db: Session = Depends(get_db), user_id = Depends(oauth.get_current_user)):
    # * %s protects us from SQL injections
    # We can write query like INSERT INTO posts (title, content, published) VALUSE ({title}, {content}, {published})
    # using the f string but some user can pass the SQL statements directly into these variables
    # to prevent this we use %s statement to sanitize the values coming from the user's end and then pass to the query

    # RETURNING * will return the newly created object
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published) )
    # new_post = cursor.fetchone()

    # it will store information in the database
    # conn.commit()

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
    # Let's say we have 50 fields in the Model, and it is not a good approach to pass 50 values to the model
    # what we can do it, we can unpack the post(pydantic) dictionary and pass directly to the Post Model
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    ic(new_post)
    ic(type(new_post))
    ic(new_post.title)
    return new_post  # FastAPI directly converts this into JSON


@router.get("/{id}", response_model=Post)
async def get_posts(id: int, response: Response, db: Session = Depends(get_db), user_id = Depends(oauth.get_current_user)):
    # We cannot use VALUES keyword in the select statement, this is against SQL syntax.
    # VALUES keyword is specifically designed for the INSERT Statements
    # cursor.execute("SELECT * FROM posts WHERE id = (%s)", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # *FIRST WAY TO SETTING RESPONSE
        # response.status_code = 404
        # return {"msg": f"Post with id {id} not found"}

        # *2nd WAY OF SETTING RESPONSE
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"msg": f"Post with id {id} not found"}

        # * 3rd OF SETTING RESPONSE
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

        # * 4th way is described in the delete method
        # in which we set the status code in the decorator
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id = Depends(oauth.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = (%s) RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        # if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    # return {"msg": "post was successfully deleted"}
    # * We donot need to return anything on delete request, even if we return anything, FastAPI will not return anything by default
    # So there is no point of writing return statement on delete request
    post.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def update_post(id: int, post: PostBase, db: Session = Depends(get_db), user_id = Depends(oauth.get_current_user)):
    # cursor.execute(
    #     "UPDATE posts SET title=%s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, id),
    # )
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_updated = post_query.first()

    if post_updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    post_query.update(post.model_dump(exclude="rating"), synchronize_session=False)
    db.commit()
    return post_query.first()