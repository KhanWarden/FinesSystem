from pathlib import Path
import aiosqlite

project_folder = Path(__file__).parent.parent.parent
DB_FILE = project_folder / "certificates.db"


async def create_certificate(date):
    async with aiosqlite.connect(DB_FILE) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""INSERT INTO certificates (date, is_used) VALUES (?, FALSE)""",
                             (date,))
        cert_id = cursor.lastrowid
        await conn.commit()
        await conn.close()

        return cert_id, date


async def is_used_certificate(cert_id: int) -> bool:
    async with aiosqlite.connect(DB_FILE) as conn:
        cursor = await conn.cursor()

        await cursor.execute("""SELECT is_used FROM certificates WHERE id = ?""",
                             (cert_id,))
        result = await cursor.fetchone()

        if result is None:
            return True

        is_used = result[0]
        if is_used:
            return True
        else:
            await cursor.execute("""UPDATE certificates SET is_used = TRUE WHERE id = ?""",
                                 (cert_id,))
            await conn.commit()
            await conn.close()
            return False
