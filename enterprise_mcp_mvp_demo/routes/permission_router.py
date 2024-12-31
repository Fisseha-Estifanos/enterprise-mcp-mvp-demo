"""
This file contains the routes for the permission router.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from playground.rbac_claude.manager import Manager

permission_router = APIRouter(prefix="/permissions", tags=["permissions"])
manager = Manager()


class PermissionCreate(BaseModel):
    """
    Pydantic model for creating a new permission.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    name: str


class PermissionResponse(BaseModel):
    """
    Pydantic model for permission response.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    id: int
    name: str

    class Config:
        orm_mode = True


@permission_router.post("/", response_model=PermissionResponse)
def create_permission(permission: PermissionCreate):
    """
    Create a new permission.

    Args:
        permission (PermissionCreate): The permission to create.

    Raises:
        HTTPException: The permission could not be created.

    Returns:
        PermissionHierarchy: The created permission.
    """
    try:
        return manager.create_permission(permission=permission.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@permission_router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: int):
    """
    Get a permission by ID.

    Args:
        permission_id (int): The ID of the permission to get.

    Raises:
        HTTPException: The permission could not be found.

    Returns:
        PermissionHierarchy: The permission.
    """
    try:
        return manager.get_permission(permission_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@permission_router.get("/", response_model=list[PermissionResponse])
def get_permissions():
    """
    Get all permissions in the system.

    Returns:
        List[PermissionHierarchy]: All permissions in the system.
    """
    try:
        return manager.get_permissions()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@permission_router.post("/add/{role_id}/{permission_id}")
def add_permission_to_role(role_id: int, permission_id: int):
    """
    Add a permission to a role.

    Args:
        role_id (int): The ID of the role to add the permission to.
        permission_id (int): The ID of the permission to add to the role.

    Raises:
        HTTPException: The permission could not be added to the role.
    """
    try:
        manager.add_permission_to_role(role_id, permission_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
