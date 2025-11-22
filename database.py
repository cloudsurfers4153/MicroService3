import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Macbook
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "mysql+pymysql://root@localhost:3306/ms3_reviews",
# )
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://ms3user:Pass123!@localhost:3306/ms3_reviews",
)


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy models."""
    pass


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """FastAPI dependency that provides a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
