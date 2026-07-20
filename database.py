import aiosqlite

DATABASE = "data/guardiao.db"


async def iniciar_banco():
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY,
            nome TEXT,
            username TEXT,
            primeira_vez TEXT,
            ultima_vez TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS entradas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            grupo_id INTEGER,
            grupo_nome TEXT,
            data TEXT
        )
        """)

        await db.commit()