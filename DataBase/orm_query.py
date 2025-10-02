from typing import Any, Dict
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Models import Attributes

# Здесь пропишем все запросы удаления, добавления, изменения (асинхронка)


async def orm_add(session: AsyncSession, table) -> None:
    session.add(table)
    await session.commit()
    
    
async def orm_get_all_cards(session: AsyncSession) -> Dict[str, Any]:
    query = select(Attributes)
    result = await session.execute(query)
    return result.scalars().all()
    
    
async def orm_get_card(session: AsyncSession, id_: int) -> Dict[str, Any]:
    query = select(Attributes).where(Attributes.id_telegram_user == id_)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_card(session: AsyncSession, id_: int, table_data) -> None:
    
    # Преобразовать в СЛОВАРИК перед отправкой, целым пакетом (классом) не получится
    
    dictionary = {attr: getattr(table_data, attr) for attr in table_data.__dict__ if not attr.startswith("_")}
    query = update(Attributes).where(Attributes.id_telegram_user == id_).values(dictionary)
    await session.execute(query)
    await session.commit()
    
    
async def orm_delete_card(session: AsyncSession, id_: int) -> None:
    query = delete(Attributes).where(id_ == Attributes.id_telegram_user)
    await session.execute(query)
    await session.commit()


