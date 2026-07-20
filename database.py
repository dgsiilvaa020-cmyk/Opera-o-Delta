import aiosqlite

DATABASE = "guardiao.db"


async def iniciar_banco():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            username TEXT,
            primeira_vez TEXT,
            ultima_vez TEXT
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS entradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            grupo_id INTEGER,
            grupo_nome TEXT,
            data TEXT
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS blacklist (
            usuario_id INTEGER PRIMARY KEY,
            motivo TEXT,
            data TEXT
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS whitelist (
            usuario_id INTEGER PRIMARY KEY,
            data TEXT
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS historico_nomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nome TEXT,
            data TEXT
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS historico_usernames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            username TEXT,
            data TEXT
        )
        """)


        await db.commit()


        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        tabelas = await cursor.fetchall()

        print("TABELAS CRIADAS:")

        for tabela in tabelas:
            print(" -", tabela[0])
            

        cursor = await db.execute("""
            SELECT * FROM historico_usernames
        """)

        dados = await cursor.fetchall()

        print("HISTORICO USERNAMES:")
        print(dados)


    print("Banco iniciado!")
