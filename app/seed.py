from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Document

USERS = [
    User(id=UUID("11111111-1111-1111-1111-111111111111"), name="Alice"),
    User(id=UUID("22222222-2222-2222-2222-222222222222"), name="Bob"),
    User(id=UUID("33333333-3333-3333-3333-333333333333"), name="Carol"),
]

DOCUMENTS = [
    Document(id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"), title="Q1 Report"),
    Document(id=UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"), title="Product Roadmap"),
    Document(id=UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"), title="Budget 2026"),
]

async def seed(session: AsyncSession):
    session.add_all(USERS)
    session.add_all(DOCUMENTS)
    await session.commit()
