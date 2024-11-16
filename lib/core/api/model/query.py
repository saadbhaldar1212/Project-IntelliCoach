from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    """
    Request model to represent incoming query request.
    """
    incoming_query: str

    class Config:
        json_scheme_extra = {
            "example": {
                "incoming_query": ""
            }
        }

class QueryResponse(BaseModel):
    """
    Response Model to represent the AI Assistant's answer to the query
    """
    success: bool
    answer: Optional[str] = None
    error_message: Optional[str] = None
