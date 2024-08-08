from typing import Generator

from sqlalchemy.orm import Session

from pifleet.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
