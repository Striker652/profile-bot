from pydantic import BaseModel
from typing import Optional

class AskRequest(BaseModel):
    question: str                  # The user's question from the chat widget

class AskResponse(BaseModel):
    answer: str                    # The full non-streaming response
    sources: Optional[list[str]] = []  # Optional: source chunk references for debugging
