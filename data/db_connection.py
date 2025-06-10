import os
from sqlalchemy import create_engine


DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

if not DB_CONNECTION_STRING:
    raise ValueError("DB_CONNECTION_STRING is not set in the environment variables.")

engine = create_engine(DB_CONNECTION_STRING)
