from __future__ import annotations

from typing import Optional, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints


# Review ID: rev + 5 digits (e.g., rev12345)
ReviewIDType = Annotated[str, StringConstraints(pattern=r"^rev-\d{5}$")]


class ReviewBase(BaseModel):
    id: ReviewIDType = Field(
        ...,
        description="Every review has an unique id",
        json_schema_extra={"example": "rev12345"},
    )
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Users can rate a movie from 1 to 5.",
        json_schema_extra={"example": 5},
    )
    comment: str = Field(
        ...,
        description="User's comment about the movie.",
        json_schema_extra={"example": "This movie is amazing."},
    )


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "rev0001",
                    "rating": 5,
                    "comment": "This movie is amazing!",
                }
            ]
        }
    }


class ReviewCreate(ReviewBase):
    """Creation payload for a Review."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "rev0002",
                    "rating": 3,
                    "comment": "The movie’s storyline is a bit old-fashioned."
                }
            ]
        }
    }


class ReviewUpdate(BaseModel):
    """Partial update for a Review; supply only fields to change."""
    rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="A new rating for the movie (1-5).",
        json_schema_extra={"example": 4},
    )
    comment: Optional[str] = Field(
        None,
        description="An updated comment for the movie.",
        json_schema_extra={"example": "Actually, it was just okay."},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "rating": 4,
                    "comment": "Updated my opinion - it's actually quite good!"
                },
                {
                    "rating": 2
                },
                {
                    "comment": "Changed my mind about this movie."
                }
            ]
        }
    }


class ReviewRead(ReviewBase):
    """Complete review data for reading/displaying."""
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "rev12345",
                    "rating": 5,
                    "comment": "This movie is absolutely fantastic! Great acting and storyline.",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }

