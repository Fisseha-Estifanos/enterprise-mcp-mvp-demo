"""
This module contains the API routes for the association of Domains, Roles, permissions and subjects.
"""

from fastapi import APIRouter
from pydantic import BaseModel


from playground.rbac_claude.manager import Manager

association_router = APIRouter(prefix="/associations", tags=["associations"])
manager = Manager()


class AssociationCreate(BaseModel):
    """
    Pydantic model for creating a new association.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    role: str
    domain: str
    permission: str
    subject: str


class TestPermissions(BaseModel):
    """
    Pydantic model for testing permissions.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    user: str
    resource: str
    permission: str


class AssociationResponse(BaseModel):
    """
    Pydantic model for association response.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    id: int
    domain: str
    role: str
    permission: str
    match_domain_prop: str | None

    class Config:
        orm_mode = True


class RoleSubjectResponse(BaseModel):
    """
    Pydantic model for role subject response.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    role: str
    subject: str

    class Config:
        orm_mode = True


@association_router.post("/", response_model=str)
def create_association(association: AssociationCreate):
    """
    Create a new association.

    Args:
        association (AssociationCreate): The association to create.

    Raises:
        HTTPException: The association could not be created.

    Returns:
        AssociationHierarchy: The created association.
    """
    try:
        manager.create_association(
            domain_name=association.domain,
            role_name=association.role,
            permission_name=association.permission,
            subject_name=association.subject,
        )
        return "Association successfully created"
    except Exception as e:
        raise BaseException(status_code=400, detail=str(e))


@association_router.get("/", response_model=list[AssociationResponse])
def get_all_associations():
    """
    Get all associations.

    Returns:
        List[AssociationHierarchy]: All associations.
    """
    associations = manager.get_all_associations()
    if not associations:
        raise BaseException(status_code=404, detail="Associations not found")
    readable_associations = []
    for association in associations:
        readable_associations.append(AssociationResponse(**association.to_dict()))
    return readable_associations


@association_router.get("/role_subject/", response_model=list[RoleSubjectResponse])
def get_all_role_subject():
    """
    Get all role subject.

    Returns:
        List[RoleSubjectHierarchy]: All role subject.
    """
    role_subjects = manager.get_all_role_subject()
    if not role_subjects:
        raise HTTPException(status_code=404, detail="Role Subject not found")

    final_role_subjects = []
    for role_subject in role_subjects:
        final_role_subjects.append(
            RoleSubjectResponse(
                subject=role_subject[0],
                role=role_subject[1],
            )
        )
    return final_role_subjects


@association_router.post("/test_permissions/", response_model=str)
def test_permissions(test_permission: TestPermissions):
    """
    Test permissions.

    Args:
        test_permission (TestPermissions): The permissions to test.

    Returns:
        str: The result of the permission test.
    """
    result = manager.test_permissions(
        user=test_permission.user,
        resource=test_permission.resource,
        permission=test_permission.permission,
    )
    if isinstance(result, bool):
        return "Permission granted"
    return result
