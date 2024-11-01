from pathlib import Path
import aiosqlite
from typing import List, Tuple

project_folder = Path(__file__).parent.parent.parent
DB_PATH = project_folder / "database.db"


async def make_admin(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
        UPDATE employees SET is_admin = 1 WHERE telegram_id = ?;
        """, (telegram_id,))
        await conn.commit()
        await conn.close()
    return f"ID: {telegram_id} добавлен в список администраторов"


async def remove_admin_from_users(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
            UPDATE employees SET is_admin = 0 WHERE telegram_id = ?;
        """, (telegram_id,))
        await conn.commit()
        await conn.close()
        return f"<b>ID: {telegram_id}</b> удалён из списка администраторов"


async def get_all_admins() -> List:
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("""SELECT telegram_id, is_admin FROM employees WHERE is_admin = 1;""") as cursor:
            admins = await cursor.fetchall()

    return admins


async def is_admin(telegram_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""SELECT is_admin FROM employees WHERE is_admin = ?""", (telegram_id,))
        row = await cursor.fetchone()
        return row is not None and row[0] == 1
