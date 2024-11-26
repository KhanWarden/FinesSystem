from pathlib import Path
import aiosqlite

project_folder = Path(__file__).parent.parent.parent
DB_PATH = project_folder / "database.db"


async def add_user_to_barrier(username):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""INSERT INTO barrier (username) VALUES (?)""",
                                    (username,))
        await conn.commit()


async def get_unmuted_users_from_barrier():
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""SELECT username FROM barrier WHERE is_muted = FALSE""")
        result = await cursor.fetchall()
        return [row[0] for row in result]


async def get_all_users_from_barrier():
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""SELECT username FROM barrier""")
        result = await cursor.fetchall()
        return [row[0] for row in result]


async def delete_user_from_barrier(username):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""DELETE FROM barrier WHERE username = ?""",
                           (username,))
        await conn.commit()


async def mute_user(username):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""UPDATE barrier SET is_muted = TRUE WHERE username = ?""",
                           (username,))
        await conn.commit()


async def unmute_user(username):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""UPDATE barrier SET is_muted = FALSE WHERE username = ?""",
                           (username,))
        await conn.commit()
