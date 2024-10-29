from fastapi import FastAPI
from . import models
from .database import engine
from . import models
from .routes import posts, users


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "world"}


app.include_router(posts.router)
app.include_router(users.router)
