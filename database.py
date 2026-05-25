import aiosqlite
import logging
import os

logger = logging.getLogger("pullify.db")

class DBManager:
    # Check if we are in Railway (or any container) by looking for the /app/data path
    # If /app/data exists, we use it to ensure persistence across deployments
    DB_PATH = "/app/data/pullify_utils.db" if os.path.exists("/app/data") else "pullify_utils.db"

    @classmethod
    async def initialize(cls):
        """Initializes the database and ensures schema integrity."""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
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
            logger.info(f"Database successfully initialized at {cls.DB_PATH}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise e

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