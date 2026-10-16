import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# آدرس دیتابیس PostgreSQL روی سرور (یوزرنیم و پسورد خود را جایگزین کنید)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost/menufood_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()