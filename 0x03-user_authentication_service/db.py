#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise ValueError("User with this email already exists")
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by specified criteria
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found with specified criteria")
            return user
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes
        """
        user = self.find_user_by(id=user_id)

        # Check if any keyword arguments don't correspond to user attributes
        invalid_args = [arg for arg in kwargs if not hasattr(user, arg)]
        if invalid_args:
            raise ValueError(f"Invalid argument(s): {', '.join(invalid_args)}")

        # Update user's attributes
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit changes to the database
        self._session.commit()
