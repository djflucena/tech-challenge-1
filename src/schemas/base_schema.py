from datetime import datetime
from pydantic import BaseModel

class BaseResponse(BaseModel):
    source: str
    fetched_at: datetime
