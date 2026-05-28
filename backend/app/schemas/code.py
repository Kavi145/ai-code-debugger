from pydantic import BaseModel
from typing import Optional

class CodeExecutionRequest(BaseModel):
    code: str

class CodeExecutionResponse(BaseModel):
    success: bool
    output: Optional[str] = None
    error_type: Optional[str] = None
    raw_error: Optional[str] = None
    ai_explanation: Optional[str] = None
    ai_suggestion: Optional[str] = None