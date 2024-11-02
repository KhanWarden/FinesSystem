from pathlib import Path
import aiosqlite
from typing import List

project_folder = Path(__file__).parent.parent.parent
DB_PATH = project_folder / "database.db"


async def make_admin(name: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
        UPDATE employees SET is_admin = 1 WHERE name = ?;
        """, (name,))
        await conn.commit()
        await conn.close()


async def delete_admin_from_users(name: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
            UPDATE employees SET is_admin = 0 WHERE name = ?;
        """, (name,))
        await conn.commit()
        await conn.close()


async def get_admins(page: int) -> List:
    items_per_page = 5
    offset = page * items_per_page
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""SELECT name FROM employees WHERE is_admin = TRUE LIMIT ? OFFSET ?""",
                                    (items_per_page, offset))
        admins = await cursor.fetchall()
    return [admin[0] for admin in admins]


async def get_total_admins() -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("""SELECT COUNT(*) FROM employees WHERE is_admin = TRUE""") as cursor:
            total = await cursor.fetchone()
    return total[0] if total else 0


async def is_admin(telegram_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()
        await cursor.execute("""SELECT is_admin FROM employees WHERE telegram_id = ?""", (telegram_id,))
        result = await cursor.fetchone()
        return bool(result and result[0] == 1)
