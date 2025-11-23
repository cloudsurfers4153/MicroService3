from datetime import datetime
import hashlib
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Path,
    Query,
    Request,
    Response,
    status,
)
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MS3 - Reviews Service",
    description="Simple microservice for CRUD operations on movie reviews.",
    version="1.0.0",
)


def build_review_etag(review: models.Review) -> str:
    """Compute a weak ETag based on review id and updated_at."""
    payload = f"{review.id}:{review.updated_at.isoformat()}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f'W/"{digest}"'


@app.get(
    "/health",
    summary="Health check",
    description="Simple health check endpoint.",
    tags=["health"],
)
def health_check() -> dict:
    return {"status": "ok"}


@app.get(
    "/reviews",
    response_model=schemas.ReviewListResponse,
    summary="List reviews",
    description=(
        "List reviews filtered by movie, user, rating range, and creation time. "
        "Supports simple pagination."
    ),
    tags=["reviews"],
)
def list_reviews(
    movie_id: Annotated[int | None, Query(
        description="Filter by movie ID.",
        example=1,
    )] = None,
    user_id: Annotated[int | None, Query(
        description="Filter by user ID.",
        example=1,
    )] = None,
    rating_min: Annotated[int | None, Query(
        ge=1,
        le=5,
        description="Minimum rating (inclusive).",
        example=3,
    )] = None,
    rating_max: Annotated[int | None, Query(
        ge=1,
        le=5,
        description="Maximum rating (inclusive).",
        example=5,
    )] = None,
    created_before: Annotated[datetime | None, Query(
        description="Only reviews created on or before this timestamp (ISO 8601).",
        example="2025-10-10T23:59:59",
    )] = None,
    created_after: Annotated[datetime | None, Query(
        description="Only reviews created on or after this timestamp (ISO 8601).",
        example="2025-10-01T00:00:00",
    )] = None,
    page: Annotated[int, Query(
        ge=1,
        description="Page number (1-based).",
        example=1,
    )] = 1,
    page_size: Annotated[int, Query(
        ge=1,
        le=100,
        description="Number of items per page.",
        example=10,
    )] = 10,
    db: Session = Depends(get_db),
) -> schemas.ReviewListResponse:
    query = db.query(models.Review)

    if movie_id is not None:
        query = query.filter(models.Review.movie_id == movie_id)
    if user_id is not None:
        query = query.filter(models.Review.user_id == user_id)
    if rating_min is not None:
        query = query.filter(models.Review.rating >= rating_min)
    if rating_max is not None:
        query = query.filter(models.Review.rating <= rating_max)
    if created_before is not None:
        query = query.filter(models.Review.created_at <= created_before)
    if created_after is not None:
        query = query.filter(models.Review.created_at >= created_after)

    total = query.count()

    offset = (page - 1) * page_size
    reviews = (
        query
        .order_by(models.Review.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return schemas.ReviewListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=reviews,
    )


@app.post(
    "/reviews",
    response_model=schemas.ReviewRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a review",
    description="Create a new review for a specific movie and user.",
    tags=["reviews"],
)
def create_review(
    review_in: schemas.ReviewCreate,
    db: Session = Depends(get_db),
) -> schemas.ReviewRead:
    db_review = models.Review(
        movie_id=review_in.movie_id,
        user_id=review_in.user_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@app.get(
    "/reviews/{review_id}",
    response_model=schemas.ReviewRead,
    summary="Get a review by ID",
    description=(
        "Retrieve a single review by its ID. Supports optional ETag via "
        '`If-None-Match` header, returning `304 Not Modified` when matched.'
    ),
    tags=["reviews"],
)
def get_review(
    review_id: Annotated[int, Path(
        description="ID of the review to retrieve.",
        example=1,
    )],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> schemas.ReviewRead | Response:
    review = db.get(models.Review, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )

    etag = build_review_etag(review)
    if_none_match = request.headers.get("if-none-match")

    if if_none_match == etag:
        return Response(
            status_code=status.HTTP_304_NOT_MODIFIED,
            headers={"ETag": etag},
        )

    response.headers["ETag"] = etag
    return review


@app.put(
    "/reviews/{review_id}",
    response_model=schemas.ReviewRead,
    summary="Update a review",
    description="Update the rating and/or comment of an existing review.",
    tags=["reviews"],
)
def update_review(
    review_id: Annotated[int, Path(
        description="ID of the review to update.",
        example=1,
    )],
    review_in: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
) -> schemas.ReviewRead:
    review = db.get(models.Review, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )

    data = review_in.model_dump(exclude_unset=True)

    if "rating" in data:
        review.rating = data["rating"]
    if "comment" in data:
        review.comment = data["comment"]

    # Always update the timestamp on modification.
    review.updated_at = datetime.utcnow()

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@app.delete(
    "/reviews/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a review",
    description="Delete an existing review by its ID.",
    tags=["reviews"],
)
def delete_review(
    review_id: Annotated[int, Path(
        description="ID of the review to delete.",
        example=1,
    )],
    db: Session = Depends(get_db),
) -> Response:
    review = db.get(models.Review, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )

    db.delete(review)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
