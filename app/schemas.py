from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class GrantCreate(BaseModel):
    document_id: UUID
    creator_id: UUID
    grantee_id: UUID
    permission: str
    expires_at: datetime

class GrantResponse(GrantCreate):
    id: UUID
    revoked: bool

    class Config:
        from_attributes = True
