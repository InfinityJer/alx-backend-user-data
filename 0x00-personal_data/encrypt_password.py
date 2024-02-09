# encrypt_password.py

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password
