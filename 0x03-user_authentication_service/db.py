#!/usr/bin/env python3
"""Module to interact with user database"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """Database management class"""

    def __init__(self):
        """Initialize a new database instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self._session = None

    @property
    def session(self):
        """Memoized session object"""
        if self._session is None:
            DBSession = sessionmaker(bind=self._engine)
            self._session = DBSession()
        return self._session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self.session.add(user)
        self.session.commit()
        return user

    def find_user_by(self, **filters) -> User:
        """Find a user based on given filters"""
        if not User.__dict__.get(*filters):
            raise InvalidRequestError
        query = self.session.query(User).filter_by(**filters)
        if not query.first():
            raise NoResultFound
        return query.first()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes based on given arguments"""
        user_to_update = self.find_user_by(id=user_id)

        for key, val in kwargs.items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, val)
            else:
                raise ValueError("Invalid attribute")

        self.session.commit()
