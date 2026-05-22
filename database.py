# Database setup (expects sqlite, 
# if using other db please change the connect args accordingly)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from helpers.utils import grab_env_var

DATABASE_URL = grab_env_var('DATABASE_URL')

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine
)

Base = declarative_base()
