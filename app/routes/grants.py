import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal
from app.models import Grant
from app.schemas import GrantCreate
from app.services.grant_service import validate_grant

router = APIRouter(prefix="/grants", tags=["grants"])

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/")
async def create_grant(
    payload: GrantCreate,
    session: AsyncSession = Depends(get_session)
):
    await validate_grant(session, payload)

    grant = Grant(
        id=uuid.uuid4(),
        document_id=payload.document_id,
        creator_id=payload.creator_id,
        grantee_id=payload.grantee_id,
        permission=payload.permission,
        expires_at=payload.expires_at
    )

    session.add(grant)
    await session.commit()
    await session.refresh(grant)

    return grant

@router.get("/")
async def list_grants(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Grant))
    return result.scalars().all()

@router.get("/{grant_id}")
async def get_grant(
    grant_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Grant).where(Grant.id == grant_id)
    )

    grant = result.scalar()

    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")

    return grant

@router.delete("/{grant_id}")
async def revoke_grant(
    grant_id: uuid.UUID,
    creator_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Grant).where(Grant.id == grant_id)
    )

    grant = result.scalar()

    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")

    if grant.creator_id != creator_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if grant.revoked:
        raise HTTPException(status_code=400, detail="Already revoked")

    if grant.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Grant expired")

    grant.revoked = True

    await session.commit()

    return {"message": "Grant revoked"}

@router.get("/{grant_id}/check")
async def check_grant(
    grant_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Grant).where(Grant.id == grant_id)
    )

    grant = result.scalar()

    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")

    active = (
        not grant.revoked and
        grant.expires_at > datetime.utcnow()
    )

    return {"active": active}
