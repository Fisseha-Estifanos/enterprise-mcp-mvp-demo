"""
The user router module defines the FastAPI endpoint for routing user requests.

Raises:
    HTTPException: The user could not be created.
    HTTPException: The user could not be found.
"""

from typing import List
from pydantic import BaseModel
from datetime import datetime


from fastapi import APIRouter, HTTPException

from playground.rbac_claude.manager import Manager

user_router = APIRouter(prefix="/users", tags=["users"])
manager = Manager()


# Pydantic models for request/response
class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    """
    Pydantic model for user response.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # role: int ???

    class Config:
        orm_mode = True


class UserRoleUpdate(BaseModel):
    """
    Pydantic model for updating user role.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    role: int


@user_router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    Create a new user.

    Args:
        user (UserCreate): The user to create.

    Raises:
        HTTPException: The user could not be created.

    Returns:
        User: The created user.
    """
    try:
        return manager.create_user(user=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    Get a user by ID.

    Args:
        user_id (int): The user ID.

    Raises:
        HTTPException: The user could not be found.

    Returns:
        User: The user, or an HTTPException if the user could not be found.
    """
    user = manager.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/", response_model=List[UserResponse])
def get_all_users():
    """
    Get all users.

    Returns:
        List[User]: The list of all users.
    """
    return manager.get_users()


@user_router.put("/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int, role_update: UserRoleUpdate):
    """
    Update a user's role.

    Args:
        user_id (int): The user ID.
        role_update (UserRoleUpdate): The new role.

    Raises:
        HTTPException: The user could not be found.

    Returns:
        User: The updated user.
    """
    user = manager.update_user_role(user_id, role_update.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/{user_id}")
def delete_user(user_id: int):
    """
    Delete a user by ID.

    Args:
        user_id (int): The user ID.

    Raises:
        HTTPException: The user could not be found.

    Returns:
        dict: The deletion message.
    """
    if not manager.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@user_router.get("/{user_id}/can-access/{server_id}")
def check_server_access(user_id: int, server_id: int):
    """
    Check if a user can access a server.

    Args:
        user_id (int): The user ID.
        server_id (int): The server ID.

    Returns:
        dict: The result of the access check.
    """
    return {"can_access": manager.can_access_server(user_id, server_id)}
