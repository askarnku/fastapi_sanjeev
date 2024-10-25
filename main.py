from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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


@app.get("/")
def root():
    return {"Hello": "world"}


@app.get("/posts")
def root():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(payLoad: Post):
    post_dict = payLoad.model_dump()
    post_dict["id"] = randrange(1, 100000)
    my_posts.append(post_dict)
    return {"data": "Post successfully added"}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    return {"post_detail": post}


@app.get("/posts/{id}")
def update_post(id: int):
    pass


@app.delete("/posts/{id}")
def delete_post(id: int):
    print(find_post(id))
    if not delete_post_by_id(id):
        return {"error": "post does not exist"}
    return {"data": "post deleted"}
