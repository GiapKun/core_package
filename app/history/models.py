from typing import Literal, Optional

from pydantic import BaseModel


class History(BaseModel):
    document_id: Optional[str] = None
    name: str
    action: Literal["create", "update", "delete"]
    type: str
    new_data: Optional[dict] = None
    old_data: Optional[dict] = None
    created_at: float
    created_by: Optional[str] = None
