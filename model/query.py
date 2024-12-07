from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    """
    Request model to represent incoming query request.
    """
    incoming_query: str
    topics: list

    class Config:
        json_scheme_extra = {
            "example": {
                "incoming_query": "",
                "topics": []
            }
        }

class QueryResponse(BaseModel):
    """
    Response Model to represent the AI Assistant's answer to the query
    """
    success: bool
    topics: Optional[list] = None
    answer: Optional[str] = None
    error_message: Optional[str] = None
