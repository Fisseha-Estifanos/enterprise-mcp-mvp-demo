"""
CRUD operations for the User, Server, and RoleHierarchy tables.

Raises:
    Exception: The error creating the user.
    Exception: The error updating the user role.
    Exception: The error deleting the user.
    Exception: The error creating the server.
    Exception: The error updating the server role.
    Exception: The error deleting the server.
    Exception: The error creating the role.
"""

import json
from typing import List, Optional

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

# from .database import get_db
from .models import User, Server, RoleHierarchy

Base = declarative_base()


def _load_configuration(config_file: str) -> dict:
    """
    Loads the configuration from a JSON file.

    Args:
        config_file (str): Path to the JSON configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON configuration: {e}")
        return {}


class DatabaseManager:
    """
    Class to manage CRUD operations for the User, Server, and RoleHierarchy tables.
    """

    def __init__(self):
        try:
            self.configuration = _load_configuration(
                config_file="configurations.json")
            # TODO : refactor this to use the database file
            self.sqlalchemy_database_url = self.configuration.get(
                "SQLALCHEMY_DATABASE_URL",
                "",
            )
            if self.sqlalchemy_database_url == "":
                print("SQLALCHEMY_DATABASE_URL not found in configurations.json")
                return
            self.engine = create_engine(
                self.sqlalchemy_database_url,
                # Only needed for SQLite
                connect_args={"check_same_thread": False},
            )
            self.session_local = sessionmaker(
                bind=self.engine,
            )
            self.db = self.session_local()
        except FileNotFoundError as e:
            print(
                f"File not found error initializing DatabaseManager: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error initializing DatabaseManager: {str(e)}")
        except SQLAlchemyError as e:
            print(f"SQLAlchemy error initializing DatabaseManager: {str(e)}")

    # User operations
    def create_user(self, username: str, role: int) -> User:
        """
        Create a new user in the database.

        Args:
            username (str): The username of the new user.
            role (int): The role level of the new user.

        Raises:
            Exception: If there is an error creating the user.

        Returns:
            User: The newly created user.
        """
        try:
            user = User(username=username, role=role)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error creating user: {str(e)}") from e

    def create_user_with_role(self, username: str, string_role: str) -> User:
        """
        Create a new user in the database with a specified role in string.

        Args:
            username (str): The username of the new user.
            string_role (str): The role level of the new user in string.

        Raises:
            Exception: If the role does not exist.

        Returns:
            User: The newly created user.
        """
        try:
            role = self.get_role_by_name(string_role)
            if not role:
                raise ValueError(f"Role {role} does not exist")
            return self.create_user(username, role.level.value)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(
                f"Error creating user with role: {str(e)}") from e

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get a user from the database by user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_name(self, username: str) -> Optional[User]:
        """
        Get a user from the database by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_all_users(self) -> List[User]:
        """
        Get all users from the database.

        Returns:
            List[User]: The list of all users.
        """
        return self.db.query(User).all()

    def update_user_role(self, user_id: int, new_role: int) -> Optional[User]:
        """
        Update the role of a user in the database.

        Args:
            user_id (int): The ID of the user to update.
            new_role (int): The new role level for the user.

        Raises:
            Exception: The error updating the user role.

        Returns:
            Optional[User]: The updated user if successful, otherwise None.
        """
        try:
            user = self.get_user(user_id)
            if user:
                user.role = new_role
                self.db.commit()
                self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error updating user role: {str(e)}") from e

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user from the database.

        Args:
            user_id (int): The ID of the user to delete.

        Raises:
            Exception: The error deleting the user.

        Returns:
            bool: The result of the deletion operation.
        """
        try:
            user = self.get_user(user_id)
            if user:
                self.db.delete(user)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error deleting user: {str(e)}") from e

    # Server operations
    def create_server(self, name: str, required_role: int) -> Server:
        """
        Create a new server in the database.

        Args:
            name (str): The name of the new server.
            required_role (int): The minimum role level required to access the server.

        Raises:
            Exception: If there is an error creating the server.

        Returns:
            Server: The newly created server.
        """
        try:
            server = Server(name=name, required_role=required_role)
            self.db.add(server)
            self.db.commit()
            self.db.refresh(server)
            return server
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error creating server: {str(e)}") from e

    def get_server(self, server_id: int) -> Optional[Server]:
        """
        Get a server from the database by server ID.

        Args:
            server_id (int): The ID of the server to retrieve.

        Returns:
            Optional[Server]: The server if found, otherwise None.
        """
        return self.db.query(Server).filter(Server.id == server_id).first()

    def get_server_by_name(self, server_name: str) -> Optional[Server]:
        """
        Get a server from the database by server name.

        Args:
            server_name (str): The name of the server to retrieve.

        Returns:
            Optional[Server]: The server if found, otherwise None.
        """
        return self.db.query(Server).filter(Server.name == server_name).first()

    def get_all_servers(self) -> List[Server]:
        """
        Get all servers from the database.

        Returns:
            List[Server]: The list of all servers.
        """
        return self.db.query(Server).all()

    def update_server_role(
        self, server_id: int, new_required_role: int
    ) -> Optional[Server]:
        """
        Update the role required to access a server in the database.

        Args:
            server_id (int): The ID of the server to update.
            new_required_role (int): The new minimum role level required to access the
            server.

        Raises:
            Exception: The error updating the server role.

        Returns:
            Optional[Server]: The updated server if successful, otherwise None.
        """
        try:
            server = self.get_server(server_id)
            if server:
                server.required_role = new_required_role
                self.db.commit()
                self.db.refresh(server)
            return server
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error updating server role: {str(e)}") from e

    def delete_server(self, server_id: int) -> bool:
        """
        Delete a server from the database.

        Args:
            server_id (int): The ID of the server to delete.

        Raises:
            Exception: The error deleting the server.

        Returns:
            bool: The result of the deletion operation.
        """
        try:
            server = self.get_server(server_id)
            if server:
                self.db.delete(server)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error deleting server: {str(e)}") from e

    # Role Hierarchy operations
    def create_role(self, role_name: str, level: int) -> RoleHierarchy:
        """
        Create a new role in the database.

        Args:
            role_name (str): The name of the new role.
            level (int): The level of the new role.

        Raises:
            Exception: The error creating the role.

        Returns:
            RoleHierarchy: The newly created role.
        """
        try:
            role = RoleHierarchy(role_name=role_name, level=level)
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            return role
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error creating role: {str(e)}") from e

    def get_role(self, role_id: int) -> Optional[RoleHierarchy]:
        """
        Get a role from the database by role ID.

        Args:
            role_id (int): The ID of the role to retrieve.

        Returns:
            Optional[RoleHierarchy]: The role if found, otherwise None.
        """
        return self.db.query(RoleHierarchy).filter(RoleHierarchy.id == role_id).first()

    def get_role_by_name(self, role_name: str) -> Optional[RoleHierarchy]:
        """
        Get a role from the database by role name.

        Args:
            role_name (str): The name of the role to retrieve.

        Returns:
            Optional[RoleHierarchy]: The role if found, otherwise None.
        """
        return (
            self.db.query(RoleHierarchy)
            .filter(RoleHierarchy.role_name == role_name)
            .first()
        )

    def get_all_roles(self) -> List[RoleHierarchy]:
        """
        Get all roles from the database.

        Returns:
            List[RoleHierarchy]: The list of all roles.
        """
        return self.db.query(RoleHierarchy).order_by(RoleHierarchy.level.desc()).all()

    # Access control helper
    def can_access_server(self, user_id: int, server_id: int) -> bool:
        """
        Check if a user can access a server based on role hierarchy

        Args:
            user_id (int): The ID of the user.
            server_id (int): The ID of the server.

        Returns:
            bool: True if the user can access the server, False otherwise.
        """
        user = self.get_user(user_id)
        server = self.get_server(server_id)
        if user and server:
            return user.role >= server.required_role
        return False
