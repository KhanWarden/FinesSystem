import asyncpg


class AdminDatabase:
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    async def create(cls, **db_config):
        pool = await asyncpg.create_pool(**db_config)
        return cls(pool)

    async def add_admin_from_users(self, user_id):
        async with self.pool.acquire() as conn:
            check_user = """
                SELECT name FROM users WHERE telegram_id = $1
            """
            user = await conn.fetchrow(check_user, user_id)

            if not user:
                raise ValueError(f'User {user_id} not found')

            add_admin = """
            INSERT INTO admins (telegram_id, user_id)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO NOTHING
            """
            await conn.execute(add_admin, user_id, user['name'])
            return f"Admin {user_id} added"

    async def remove_admin_from_users(self, user_id):
        async with self.pool.acquire() as conn:
            remove_admin = """
            DELETE FROM admins WHERE telegram_id = $1
            """
            user = await conn.fetchrow(remove_admin, user_id)
            if not user:
                raise ValueError(f'User {user_id} not found')

            await conn.execute(remove_admin, user_id)
            return f"Admin {user_id} removed"

    async def get_all_admins(self):
        async with self.pool.acquire() as conn:
            admins = await conn.fetch("SELECT * FROM admins")
            return admins
