from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schema, models, oauth2
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schema.ResponsePost])
@router.get("/", response_model=List[schema.PostOut])
# @router.get("/")
def root(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # Retrieve all posts from the database
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.ilike(f"%{search}%"))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    # by default 'join()' on alchemy is left inner join
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.ilike(f"%{search}%"))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    posts = [schema.PostOut(Post=post, votes=votes) for post, votes in results]

    return posts  # FastAPI will serialize each `Post` to match `ResponsePost`


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schema.ResponsePost
)
def create_posts(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""
    @router.post("/", response_model=schemas.Post)
    def create_post(post: schemas.PostCreate, 
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
        new_post = models.Post(owner_id=current_user.id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
"""


@router.get("/{id}", response_model=schema.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    # post = schema.PostOut(Post=result.post, votes=result.votes)
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schema.ResponsePost,
)
def update_post(
    id: int,
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    print("we reached here")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)
    return existing_post
