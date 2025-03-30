from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:1234@localhost:5555/mydatabase"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocomit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db #Tra ve session cho request su dung
    finally:
        db.close()


