from typing import Any, Dict
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Models import Attributes

# Здесь пропишем все запросы удаления, добавления, изменения (асинхронка)


async def orm_add(session: AsyncSession, table) -> None:
    session.add(table)
    session.commit()
    
    
async def orm_get_all_cards(session: AsyncSession) -> Dict[str, Any]:
    query = select(Attributes)
    result = await session.execute(query)
    return result.scalars().all()
    
    
async def orm_get_card(session: AsyncSession, id: int) -> Dict[str, Any]:
    query = select(Attributes).where(id == table.id_telegram_user)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_card(session: AsyncSession, id: int, table_data) -> None:
    query = update(Attributes).where(id == Attributes.id_telegram_user).values(table_data)
    result = await session.execute(query)
    await session.commit()
    
    
async def orm_delete_card(session: AsyncSession, id: int) -> None:
    query = delete(Attributes).where(id == Attributes.id_telegram_user)
    await session.execute(query)
    await session.commit()


