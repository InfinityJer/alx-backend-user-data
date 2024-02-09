#!/usr/bin/env python3
"""password encryption module.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    # Use bcrypt to check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)
