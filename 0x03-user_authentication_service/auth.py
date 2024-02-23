#!/usr/bin/env python3
"""A module containing authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a given password.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID.

    Returns:
        str: The generated UUID.
    """
    return str(uuid4())


class Auth:
    """A class to interact with the authentication database."""

    def __init__(self):
        """Initializes a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user in the database.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The registered user.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Union[User, None]: The corresponding user or None if not found.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session associated with a given user.

        Args:
            user_id (int): The ID of the user.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.
        
        Raises:
            ValueError: If the user does not exist.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError(f"User with email {email} does not exist")
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given the user's reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError("Invalid reset token")
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
