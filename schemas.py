from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    """Common review fields."""
    movie_id: int = Field(
        ...,
        description="ID of the movie being reviewed.",
        example=1,
    )
    user_id: int = Field(
        ...,
        description="ID of the user who wrote the review.",
        example=1,
    )
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Numeric rating from 1 (worst) to 5 (best).",
        example=5,
    )
    comment: str = Field(
        ...,
        description="Free text comment for the review.",
        example='I was not prepared for how hard "Tötet nicht mehr" would hit me; '
                'watching the father break after his son is killed during a peaceful '
                'reading made the anti death penalty message feel painfully real.',
    )


class ReviewCreate(ReviewBase):
    """Request body for creating a new review."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "movie_id": 1,
                "user_id": 1,
                "rating": 5,
                "comment": 'I was not prepared for how hard "Tötet nicht mehr" would hit me; '
                           'watching the father break after his son is killed during a peaceful '
                           'reading made the anti death penalty message feel painfully real.',
            }
        }
    )


class ReviewUpdate(BaseModel):
    """Request body for updating an existing review (rating and/or comment)."""
    rating: int | None = Field(
        None,
        ge=1,
        le=5,
        description="New rating from 1 (worst) to 5 (best).",
        example=4,
    )
    comment: str | None = Field(
        None,
        description="Updated comment for the review.",
        example='"Tötet nicht mehr" stays with me even more after a second viewing.',
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 4,
                "comment": '"Tötet nicht mehr" stays with me even more after a second viewing.',
            }
        }
    )


class ReviewInDBBase(ReviewBase):
    """Base model for reading review data from DB."""
    id: int = Field(
        ...,
        description="Review ID.",
        example=1,
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp.",
        example="2025-10-01T20:00:00",
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp.",
        example="2025-10-01T20:00:00",
    )

    model_config = ConfigDict(from_attributes=True)


class ReviewRead(ReviewInDBBase):
    """Response model for a single review."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "movie_id": 1,
                "user_id": 1,
                "rating": 5,
                "comment": 'I was not prepared for how hard "Tötet nicht mehr" would hit me; '
                           'watching the father break after his son is killed during a peaceful '
                           'reading made the anti death penalty message feel painfully real.',
                "created_at": "2025-10-01T20:00:00",
                "updated_at": "2025-10-01T20:00:00",
            }
        },
    )


class ReviewListResponse(BaseModel):
    """Paginated list of reviews."""
    total: int = Field(
        ...,
        description="Total number of reviews matching the filters.",
        example=40,
    )
    page: int = Field(
        ...,
        ge=1,
        description="Current page number (1-based).",
        example=1,
    )
    page_size: int = Field(
        ...,
        ge=1,
        description="Number of items per page.",
        example=10,
    )
    items: list[ReviewRead] = Field(
        ...,
        description="List of review items for this page.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 2,
                "page": 1,
                "page_size": 2,
                "items": [
                    {
                        "id": 1,
                        "movie_id": 1,
                        "user_id": 1,
                        "rating": 5,
                        "comment": 'I was not prepared for how hard "Tötet nicht mehr" would hit me; '
                                   'watching the father break after his son is killed during a peaceful '
                                   'reading made the anti death penalty message feel painfully real.',
                        "created_at": "2025-10-01T20:00:00",
                        "updated_at": "2025-10-01T20:00:00",
                    },
                    {
                        "id": 2,
                        "movie_id": 1,
                        "user_id": 2,
                        "rating": 3,
                        "comment": '"Tötet nicht mehr" is clearly important and the images are powerful, '
                                   'but the slow expressionist pacing and heavy melodrama kept me at a '
                                   'distance even while I admired what it was saying.',
                        "created_at": "2025-10-01T22:00:00",
                        "updated_at": "2025-10-01T22:00:00",
                    },
                ],
            }
        },
    )
