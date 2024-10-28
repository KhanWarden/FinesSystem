import sqlite3


class AdminDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_admin_from_users(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name FROM users WHERE telegram_id = ?
            """, (user_id,))
            user = cursor.fetchone()

            if user is None:
                raise ValueError(f'User {user_id} not found')

            cursor.execute("""
                INSERT INTO admins (telegram_id, user_id)
                VALUES (?, ?)
                ON CONFLICT (user_id) DO NOTHING
            """, (user_id, user[0]))
            conn.commit()

            return f"Admin {user_id} added"

    def remove_admin_from_users(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM admins WHERE telegram_id = ?
            """, (user_id,))
            conn.commit()

            return f"Admin {user_id} removed"

    def get_all_admins(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admins")
            admins = cursor.fetchall()
            return admins
