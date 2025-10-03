from __future__ import annotations

import os

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI
from fastapi import Query
from typing import Optional

from models.review import ReviewCreate, ReviewRead, ReviewUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
reviews: Dict[UUID, ReviewRead] = {}

app = FastAPI(
    title="Interaction API",
    description="Demo FastAPI app using Pydantic v2 models for Interaction",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Review endpoints
# -----------------------------------------------------------------------------
@app.post("/reviews", response_model=ReviewRead, status_code=201)
def create_review(review: ReviewCreate):
    return {"message": "NOT IMPLEMENTED - POST"}

@app.get("/reviews", response_model=List[ReviewRead])
def list_reviews(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    return {"message": "NOT IMPLEMENTED - GET"}

@app.get("/reviews/{review_id}", response_model=ReviewRead)
def get_review(review_id: UUID):
    return {"message": "NOT IMPLEMENTED - GET by id"}

@app.patch("/reviews/{review_id}", response_model=ReviewRead)
def update_review(review_id: UUID, update: ReviewUpdate):
    return {"message": "NOT IMPLEMENTED - Patch by id"}

@app.delete("/reviews/{review_id}", status_code=204)
def delete_student(student_id: UUID):
    return {"message": "NOT IMPLEMENTED - DELETE by id"}

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Interaction API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
