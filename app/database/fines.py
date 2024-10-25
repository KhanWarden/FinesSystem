import asyncpg


class FinesDatabase:
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    async def create(cls, **db_config):
        pool = await asyncpg.create_pool(**db_config)
        return cls(pool)

    async def add_fine_case(self, employee_id, fine_id):
        async with self.pool.acquire() as conn:
            query_count = """
                SELECT COUNT(*) 
                FROM employees_fines 
                WHERE telegram_id = $1 AND fine_id = $2
            """
            fine_count = await conn.fetchval(query_count, employee_id, fine_id)

            query_fine_amount = """
                SELECT amount_first, amount_second, amount_more 
                FROM fines 
                WHERE fine_id = $1
            """
            fine_info = await conn.fetchrow(query_fine_amount, fine_id)

            if fine_count == 0:
                fine_amount = fine_info['amount_first']
            elif fine_count == 1:
                fine_amount = fine_info['amount_second']
            else:
                fine_amount = fine_info['amount_more']

            query_add_fine = """
                INSERT INTO employees_fines (telegram_id, fine_id, fine_date, comments)
                VALUES ($1, $2, CURRENT_TIMESTAMP, 'Автоштраф')
            """
            await conn.execute(query_add_fine, employee_id, fine_id)
            return fine_amount

    async def get_statistics(self):
        async with self.pool.acquire() as conn:
            query_stats = """
                SELECT employees.name AS employee_name, fines.name AS fine_name, COUNT(*) AS fine_count
                FROM employees_fines
                JOIN employees ON employees_fines.telegram_id = employees.telegram_id
                JOIN fines ON employees_fines.fine_id = fines.fine_id
                GROUP BY employees.name, fines.name
            """
            rows = await conn.fetch(query_stats)
            return rows
