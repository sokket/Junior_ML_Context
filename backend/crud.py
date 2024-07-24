from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Word

async def get_words(db: AsyncSession):
    result = await db.execute(select(Word))
    return result.scalars().all()
