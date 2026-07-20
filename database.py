import aiosqlite

DATABASE = "guardiao.db"


async def iniciar_banco():
    async with aiosqlite.connect(DATABASE) as db:

        # Usuários
        await db.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            username TEXT,
            primeira_vez TEXT,
            ultima_vez TEXT
        )
        """)

        # Histórico de entradas
        await db.execute("""
        CREATE TABLE IF NOT EXISTS entradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            grupo_id INTEGER,
            grupo_nome TEXT,
            data TEXT
        )
        """)

        # Lista Negra
        await db.execute("""
        CREATE TABLE IF NOT EXISTS blacklist (
            usuario_id INTEGER PRIMARY KEY,
            motivo TEXT,
            data TEXT
        )
        """)

        # Lista Branca
        await db.execute("""
        CREATE TABLE IF NOT EXISTS whitelist (
            usuario_id INTEGER PRIMARY KEY,
            data TEXT
        )
        """)

        await db.commit()
