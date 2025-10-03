from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}

app = FastAPI(
    title="Interaction API",
    description="Demo FastAPI app using Pydantic v2 models for Interaction",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    return {"message": "NOT IMPLEMENTED - POST"}

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
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

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    return {"message": "NOT IMPLEMENTED - GET by id"}

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    return {"message": "NOT IMPLEMENTED - Patch by id"}

@app.delete("/persons/{person_id}", status_code=204)
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
