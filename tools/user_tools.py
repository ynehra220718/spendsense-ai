import json
from pathlib import Path

PROFILES_DIR = Path(__file__).parent.parent / "data" / "mock_user_profiles"


def load_user_profile(user_id: str) -> dict | None:
    path = PROFILES_DIR / f"{user_id}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def list_user_profiles() -> list[str]:
    return [p.stem for p in PROFILES_DIR.glob("*.json")]
