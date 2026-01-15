from sqlmodel import SQLModel, create_engine, Session
import os

# Database Path: Root/database/pcbbr.db
# __file__ = backend/database.py
# dirname = backend
# dirname(dirname) = Root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FOLDER = os.path.join(BASE_DIR, "database")
DB_NAME = "pcbbr.db"
DATABASE_URL = f"sqlite:///{os.path.join(DB_FOLDER, DB_NAME)}"

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    # Only for dev/testing, in prod use Alembic
    SQLModel.metadata.create_all(engine)
