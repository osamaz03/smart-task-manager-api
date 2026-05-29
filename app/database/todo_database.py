from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

DATABASE_URL = "sqlite:///./task.db"

engine = create_engine(DATABASE_URL, echo=True)

sessionlocal = sessionmaker(bind=engine)


BASE = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()