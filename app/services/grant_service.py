from datetime import datetime, timedelta
from sqlalchemy import select
from fastapi import HTTPException
from app.models import Grant

async def validate_grant(session, payload):
    if payload.expires_at <= datetime.utcnow() + timedelta(minutes=1):
        raise HTTPException(status_code=400, detail="Expiry too soon")

    existing = await session.execute(
        select(Grant).where(
            Grant.document_id == payload.document_id,
            Grant.grantee_id == payload.grantee_id,
            Grant.revoked == False,
            Grant.expires_at > datetime.utcnow()
        )
    )

    if existing.scalar():
        raise HTTPException(
            status_code=409,
            detail="Active grant already exists"
        )
