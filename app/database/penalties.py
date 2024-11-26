import sqlite3


class FinesDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_fine_case(self, employee_id, fine_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) 
                FROM employees_fines 
                WHERE telegram_id = ? AND fine_id = ?
            """, (employee_id, fine_id))
            fine_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT amount_first, amount_second, amount_more 
                FROM fines 
                WHERE fine_id = ?
            """, (fine_id,))
            fine_info = cursor.fetchone()

            if fine_info is None:
                raise ValueError(f'Fine {fine_id} not found')

            if fine_count == 0:
                fine_amount = fine_info[0]
            elif fine_count == 1:
                fine_amount = fine_info[1]
            else:
                fine_amount = fine_info[2]

            cursor.execute("""
                INSERT INTO employees_fines (telegram_id, fine_id, fine_date, comments)
                VALUES (?, ?, CURRENT_TIMESTAMP, 'Автоштраф')
            """, (employee_id, fine_id))
            conn.commit()

            return fine_amount

    def get_statistics(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT employees.name AS employee_name, fines.name AS fine_name, COUNT(*) AS fine_count
                FROM employees_fines
                JOIN employees ON employees_fines.telegram_id = employees.telegram_id
                JOIN fines ON employees_fines.fine_id = fines.fine_id
                GROUP BY employees.name, fines.name
            """)
            rows = cursor.fetchall()
            return rows
