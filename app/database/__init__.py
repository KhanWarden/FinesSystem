import aiosqlite

from .admins import (make_admin, is_admin, delete_admin_from_users, get_admins, get_total_admins,
                     get_total_non_admins, get_non_admins)
from .employees import (get_employees, add_employee, delete_employee, get_total_employees, rename_employee,
                        change_position_func)
from .certificates import create_certificate, is_used_certificate
from .barrier import (add_user_to_barrier, get_unmuted_users_from_barrier, get_all_users_from_barrier, mute_user,
                      delete_user_from_barrier, unmute_user, get_all_users_from_gate, delete_user_from_gate,
                      add_user_to_gate)


__all__ = ['init_database',
           'make_admin',
           'is_admin',
           'delete_admin_from_users',
           'get_admins',
           'get_total_admins',
           'get_non_admins',
           'get_total_non_admins',
           'get_employees',
           'get_total_employees',
           'add_employee',
           'delete_employee',
           'rename_employee',
           'change_position_func',
           'create_certificate',
           'is_used_certificate',
           'add_user_to_barrier',
           'get_all_users_from_barrier',
           'get_unmuted_users_from_barrier',
           'mute_user',
           'unmute_user',
           'delete_user_from_barrier',
           'get_all_users_from_gate',
           'add_user_to_gate',
           'delete_user_from_gate'
           ]


async def init_database():
    async with aiosqlite.connect('database.db') as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS employees (
                              telegram_id BIGINT PRIMARY KEY,
                              name VARCHAR(50) NOT NULL,
                              is_admin BOOLEAN DEFAULT 0,
                              position TEXT)""")
        await conn.execute("""CREATE TABLE IF NOT EXISTS fines (
                              fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              description TEXT,
                              amount_first INT NOT NULL,
                              amount_second INT NOT NULL,
                              amount_more INT NOT NULL)""")
        await conn.execute("""CREATE TABLE IF NOT EXISTS employees_fines (
                              fine_case_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              telegram_id BIGINT NOT NULL,
                              fine_id INT NOT NULL,
                              fine_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              comments TEXT,
                              game_id INT,
                              FOREIGN KEY (telegram_id) REFERENCES employees (telegram_id),
                              FOREIGN KEY (fine_id) REFERENCES fines (fine_id))""")
        await conn.execute("""CREATE TABLE IF NOT EXISTS barrier (
                              username TEXT PRIMARY KEY,
                              is_muted BOOLEAN DEFAULT 0)""")
        await conn.commit()
