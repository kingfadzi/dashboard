from sqlalchemy.orm import sessionmaker
from data.db_connection import engine
from profile.services.profile_loader import load_profile

SessionLocal = sessionmaker(bind=engine)

def fetch_repo_profile(repo_id):
    session = SessionLocal()
    try:
        profile_data = load_profile(session, repo_id)
    finally:
        session.close()

    return profile_data
