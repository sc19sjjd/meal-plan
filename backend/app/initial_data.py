#!/usr/bin/env python3

from app.db.crud import create_user
from app.db.schemas import UserCreate
from app.db.session import SessionLocal, get_db


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email="admin@admin.com",
            password="pass",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser admin@admin.com")
    init()
    print("Superuser created")
