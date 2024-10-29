from fastapi import FastAPI

from . import models
from .database import engine
from .routes import posts, users, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "world"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
