"""
The server_router module defines the FastAPI endpoint for managing servers.

Raises:
    HTTPException: The server could not be created.
    HTTPException: The server could not be found.
"""

from typing import List
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from db.db_manager import DatabaseManager

server_router = APIRouter(prefix="/servers", tags=["servers"])
crud = DatabaseManager()


# Pydantic models for request/response
class ServerCreate(BaseModel):
    """
    Pydantic model for creating a new server.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    name: str
    required_role: int


class ServerResponse(BaseModel):
    """
    Pydantic model for server response.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    id: int
    name: str
    required_role: int

    class Config:
        orm_mode = True


class ServerRoleUpdate(BaseModel):
    """
    Pydantic model for updating server role.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    required_role: int


@server_router.post("/", response_model=ServerResponse)
def create_server(server: ServerCreate):
    """
    Create a new server.

    Args:
        server (ServerCreate): The server to create.

    Raises:
        HTTPException: The server could not be created.

    Returns:
        Server: The created server.
    """
    try:
        return crud.create_server(name=server.name, required_role=server.required_role)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@server_router.get("/{server_id}", response_model=ServerResponse)
def get_server(server_id: int):
    """
    Get a server by ID.

    Args:
        server_id (int): The server ID to get.

    Raises:
        HTTPException: The server could not be found.

    Returns:
        Server: The server.
    """
    server = crud.get_server(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@server_router.get("/", response_model=List[ServerResponse])
def get_all_servers():
    """
    Get all servers.

    Returns:
        List[Server]: The list of all servers.
    """
    return crud.get_all_servers()


@server_router.put("/{server_id}/role", response_model=ServerResponse)
def update_server_role(server_id: int, role_update: ServerRoleUpdate):
    """
    Update a server's role.

    Args:
        server_id (int): The server ID.
        role_update (ServerRoleUpdate): The new role.

    Raises:
        HTTPException: The server could not be found.

    Returns:
        Server: The updated server.
    """
    server = crud.update_server_role(server_id, role_update.required_role)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@server_router.delete("/{server_id}")
def delete_server(server_id: int):
    """
    Delete a server by ID.

    Args:
        server_id (int): The server ID.

    Raises:
        HTTPException: The server could not be found.

    Returns:
        dict: The deletion message.
    """
    if not crud.delete_server(server_id):
        raise HTTPException(status_code=404, detail="Server not found")
    return {"message": "Server deleted successfully"}
