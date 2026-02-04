import sqlite3


class Database:
    def __init__(self, db_path="bot.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    user_id INTEGER PRIMARY KEY,
                    category TEXT
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    user_id INTEGER PRIMARY KEY
                )
            ''')

            conn.commit()

    def toggle_subscription(self, user_id: int, category: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT category FROM subscriptions WHERE user_id = ?", (user_id,)
            )
            current = cursor.fetchone()

            if current and current[0] == category:
                conn.execute(
                    "DELETE FROM subscriptions WHERE user_id = ?", (user_id,)
                )
                new_status = None
            else:
                conn.execute(
                    "INSERT OR REPLACE INTO subscriptions VALUES (?, ?)", (user_id, category)
                )
                new_status = category

            conn.commit()
            return new_status

    def get_subscription(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT category FROM subscriptions WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            return row[0] if row else None