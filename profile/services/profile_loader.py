import json
from sqlalchemy.orm import Session
from profile.models.repo_profile_cache import RepoProfileCache

def load_profile(session: Session, repo_id: str):
    cached = session.query(RepoProfileCache).filter_by(repo_id=repo_id).first()
    if not cached:
        raise ValueError(f"No cached profile found for repo_id={repo_id}")

    return json.loads(cached.profile_json)