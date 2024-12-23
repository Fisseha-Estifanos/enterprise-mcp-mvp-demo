"""
Module to define the FastAPI endpoint for routing incoming requests.

Returns:
    dict: The response message.
"""

from pydantic import BaseModel

from fastapi import APIRouter

from routing.request_router import RequestRouter


# FastAPI app instance
request_router = APIRouter(prefix="/request", tags=["roles"])
router = RequestRouter(config_file="configurations.json")


# Request payload model
class QuestionRequest(BaseModel):
    """
    Pydantic model for incoming question requests.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    username: str
    question: str


# FastAPI endpoint
@request_router.post("/route")
async def route_incoming_request(request: QuestionRequest):
    """
    Endpoint to route user requests using RequestRouter.

    Args:
        request (QuestionRequest): The incoming request.

    Returns:
        dict: The response message.
    """
    return await router.route_request(
        username=request.username,
        question=request.question,
    )
