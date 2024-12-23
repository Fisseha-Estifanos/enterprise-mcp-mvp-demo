"""
SQLAlchemy models for the database tables.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    User table to store user information.

    Args:
        id (int): Primary key.
        username (str): User's username.
        role (int): User's role level.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    role = Column(Integer, nullable=False)  # Will map to RoleHierarchy level


class Server(Base):
    """
    Server table to store server names and the minimum role level required to access
    them.

    Args:
        id (int): Primary key.
        name (str): Server name.
        required_role (int): Minimum role level required to access the server.
    """

    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    # Minimum role level required
    required_role = Column(Integer, nullable=False)


class RoleHierarchy(Base):
    # generate a docstring for the class
    """
    Role hierarchy table to store role names and their corresponding levels.

    Args:
        id (int): Primary key.
        role_name (str): Role name.
        level (int): Role level.
    """
    __tablename__ = "role_hierarchy"

    id = Column(Integer, primary_key=True)
    role_name = Column(
        String(50), unique=True, nullable=False
    )  # e.g., 'admin', 'user', 'system'
    level = Column(
        Integer, unique=True, nullable=False
    )  # Higher number = higher access
