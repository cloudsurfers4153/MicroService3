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
    uni: Optional[ReviewIDType] = Field(
        None, description="Columbia UNI.", json_schema_extra={"example": "ab1234"}
    )
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Augusta"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "King"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "ada@newmail.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+44 20 7946 0958"})
    birth_date: Optional[date] = Field(None, json_schema_extra={"example": "1815-12-10"})


    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Ada", "last_name": "Byron"},
                {"phone": "+1-415-555-0199"},
                {
                    "addresses": [
                        {
                            "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                            "street": "10 Downing St",
                            "city": "London",
                            "state": None,
                            "postal_code": "SW1A 2AA",
                            "country": "UK",
                        }
                    ]
                },
            ]
        }
    }


class ReviewRead(ReviewBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Review ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
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
                    "id": "99999999-9999-4999-8999-999999999999",
                    "uni": "abc1234",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "email": "ada@example.com",
                    "phone": "+1-212-555-0199",
                    "birth_date": "1815-12-10",
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "123 Main St",
                            "city": "London",
                            "state": None,
                            "postal_code": "SW1A 1AA",
                            "country": "UK",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
