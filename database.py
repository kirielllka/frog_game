from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = str(os.getenv('DB_URL'))

engine = create_engine(DATABASE_URL)

session_maker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

class Base(DeclarativeBase):
    pass