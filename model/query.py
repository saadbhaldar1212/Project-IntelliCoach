"""Query request and response models for the fitness advisor API.

Defines Pydantic models for validating and serializing API requests and responses.
"""

from typing import Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    """
    Request model to represent incoming query request.
    """

    incoming_query: str
    topics: list

    class Config:
        """
        Custom Example for QueryRequest.
        """

        json_schema_extra = {
            "example": {"incoming_query": "Hello", "topics": ["Health"]}
        }


class QueryResponse(BaseModel):
    """
    Response Model to represent the AI Assistant's answer to the query
    """

    success: bool
    topics: Optional[list] = None
    answer: Optional[str] = None
    error_message: Optional[str] = None
    source: Optional[str] = None
