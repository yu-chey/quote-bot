import aiosqlite

from src.config import db_path

async def add_quote(quote_text) -> None:
    async with aiosqlite.connect(database=db_path) as connect:
        cursor = await connect.cursor()

        await connect.execute("INSERT INTO quotes (quote_text) VALUES (?);",
                              (quote_text,))
        await connect.commit()

async def select_all() -> list[str]:
    async with aiosqlite.connect(database=db_path) as connect:
        cursor = await connect.cursor()

        quotes = await cursor.execute("SELECT * FROM quotes")

        return await quotes.fetchall()

async def delete_quote(quote_id: int) -> bool:
    try:
        async with aiosqlite.connect(database=db_path) as connect:
            cursor = await connect.execute(
                "DELETE FROM quotes WHERE id = ?",
                (quote_id,)
            )

            await connect.commit()

            rows_deleted = cursor.rowcount

            return rows_deleted > 0

    except Exception as e:
        print(f"Ошибка при удалении цитаты: {e}")
        return False

async def create_table_quotes() -> None:
    async with aiosqlite.connect(database=db_path) as connect:
        await connect.execute('''
            CREATE TABLE IF NOT EXISTS "quotes" (
                "id"	INTEGER NOT NULL UNIQUE,
                "quote_text"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        ''')
        await connect.commit()