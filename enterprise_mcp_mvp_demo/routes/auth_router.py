"""
The authentication router module defines the FastAPI endpoint for routing user's
authentication requests.

Raises:
"""

from typing import List
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from playground.rbac_claude.manager import Manager

auth_router = APIRouter(prefix="/auth", tags=["users"])
manager = Manager()


# Pydantic models for request/response
class Login(BaseModel):
    """
    Pydantic model for a login.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    username: str
    password: str


class Signin(BaseModel):
    """
    Pydantic model for a Signup.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    id: int
    username: str
    role: int


@auth_router.post("/login")
def login(user: Login):
    """
    Login a user.

    Args:
        user (Login): The user to login.
    """
    try:
        try:
            # Authenticate user
            authenticated_user = manager.user_service.authenticate(
                user.username,
                user.password,
            )
            print(f"Authenticated user: {authenticated_user.to_dict()}")
            return authenticated_user
        except ValueError as e:
            print(f"Error authenticating: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
