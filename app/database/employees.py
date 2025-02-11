from pathlib import Path
import aiosqlite

project_folder = Path(__file__).parent.parent.parent
DB_PATH = project_folder / "database.db"


async def get_employees(page: int):
    items_per_page = 5
    offset = page * items_per_page
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""SELECT name FROM employees LIMIT ? OFFSET ?""",
                                    (items_per_page, offset))
        employees = await cursor.fetchall()
    return [employee[0] for employee in employees]


async def get_total_employees() -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("""SELECT COUNT(*) FROM employees""") as cursor:
            total = await cursor.fetchone()
    return total[0] if total else 0


async def add_employee(telegram_id: int, name: str, position: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""SELECT 1 FROM employees WHERE name = ?""", (name,))
        exists = await cursor.fetchone()

        if exists:
            await conn.close()
            return False

        await cursor.execute("""INSERT INTO employees (telegram_id, name, is_admin, position) VALUES (?, ?, FALSE, ?)""",
                             (telegram_id, name, position))
        await conn.commit()
        await conn.close()

    return True


async def delete_employee(employee_name: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()
        await cursor.execute("""DELETE FROM employees WHERE name = ?""", (employee_name,))
        await conn.commit()
        await conn.close()


async def rename_employee(employee_name: str, new_name: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""SELECT 1 FROM employees WHERE name = ?""", (new_name,))
        exists = await cursor.fetchone()

        if exists:
            await conn.close()
            return False

        await cursor.execute("""UPDATE employees SET name = ? WHERE name = ?""", (new_name, employee_name))
        await conn.commit()
        await conn.close()
    return True


async def change_position_func(employee_name: str, new_position: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()
        await cursor.execute("""UPDATE employees SET position = ? WHERE name = ?""",
                             (new_position, employee_name))
        await conn.commit()
        await conn.close()