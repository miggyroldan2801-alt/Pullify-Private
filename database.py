import sqlite3
import asyncio
import logging

class DBManager:
    DB_PATH = "pullify_utils.db"

    @classmethod
    async def initialize(cls):
        async with aiosqlite.connect(cls.DB_PATH) as db:
            # Tickets Table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    thread_id INTEGER,
                    reason TEXT,
                    status TEXT DEFAULT 'open'
                )
            """)
            await db.commit()

    @classmethod
    async def create_ticket(cls, user_id, thread_id, reason):
        async with aiosqlite.connect(cls.DB_PATH) as db:
            cursor = await db.execute(
                "INSERT INTO tickets (user_id, thread_id, reason) VALUES (?, ?, ?)",
                (user_id, thread_id, reason)
            )
            await db.commit()
            return cursor.lastrowid

    @classmethod
    async def update_ticket_status(cls, thread_id, status):
        async with aiosqlite.connect(cls.DB_PATH) as db:
            await db.execute(
                "UPDATE tickets SET status = ? WHERE thread_id = ?",
                (status, thread_id)
            )
            await db.commit()