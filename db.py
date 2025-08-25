import aiosqlite

DB_PATH = "portfolio.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                user_id INTEGER,
                asset TEXT,
                amount REAL,
                buy_price REAL DEFAULT 0
            )
        """)
        await db.commit()

async def add_asset(user_id: int, asset: str, amount: float, buy_price: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO portfolio (user_id, asset, amount, buy_price)
            VALUES (?, ?, ?, ?)
        """, (user_id, asset, amount, buy_price))
        await db.commit()

async def get_portfolio(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT asset, amount, buy_price FROM portfolio
            WHERE user_id = ?
        """, (user_id,))
        rows = await cursor.fetchall()
        return [row for row in rows if len(row) == 3]

async def reset_portfolio(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM portfolio WHERE user_id = ?", (user_id,))
        await db.commit()
