from core.database import get_user_collection
from core.utils import hash_password, verify_password

from datetime import datetime

users_col = get_user_collection()

def register_user(email: str, password: str) -> bool:
    if users_col.find_one({"email": email}):
        return False

    hashed = hash_password(password)

    users_col.insert_one({
        "email": email,
        "password": hashed,
        "created_at": datetime.utcnow()
    })
    return True


def login_user(email: str, password: str) -> bool:
    user = users_col.find_one({"email": email})
    if not user:
        return False

    return verify_password(password, user["password"])

