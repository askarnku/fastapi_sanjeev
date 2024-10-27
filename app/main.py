from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DB connected")
        break
    except Exception as error:
        print("Connection failed")
        print(error)
        time.sleep(2)


my_posts = [
    {"title": "title of the post", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


def delete_post_by_id(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            del my_posts[index]
            return True
    return False


def find_post_by_index(id: int):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return -1


@app.get("/")
def root():
    return {"Hello": "world"}


@app.get("/posts")
def root():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()

    conn.commit()
    return {"data": new_post}


# @app.get("/posts/{id}")
# def get_post(id: int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
#         )
#     return {"post_detail": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    return {"post_detail": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     print(find_post(id))
#     if not delete_post_by_id(id):
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update_post(id: int, body: Post):
#     # client is sending id of the post and requesting to update that post with new body
#     # 1. convert to dictionary the response body
#     index = find_post_by_index(id)
#     if index < 0:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {id} was not found",
#         )
#     post_dict = body.model_dump()
#     post_dict["id"] = id
#     my_posts[index] = post_dict
#     return {"message": f"post with id: {id} was updated"}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    # client is sending id of the post and requesting to update that post with new body
    # 1. convert to dictionary the response body

    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s
                    WHERE id = %s
                    RETURNING * """,
        (
            post.title,
            post.content,
            post.published,
            id,
        ),
    )
    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    conn.commit()
    return {"message": updated_post}
