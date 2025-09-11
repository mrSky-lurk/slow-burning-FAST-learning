from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:0302@localhost:5432/fast_api_db"
engine = create_engine(db_url)
LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)