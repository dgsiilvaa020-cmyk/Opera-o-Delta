import os
import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import iniciar_banco
from aiogram import F
from aiogram.types import ChatMemberUpdated
from datetime import datetime
import aiosqlite

# Cria o bot
bot = Bot(token=BOT_TOKEN)

# Dispatcher
dp = Dispatcher()


DATABASE = "guardiao.db"


@dp.chat_member()
async def novo_membro(event: ChatMemberUpdated):

@dp.chat_member()
async def novo_membro(event: ChatMemberUpdated):

    print("EVENTO CHAT_MEMBER RECEBIDO")


    # Só executa quando alguém entra no grupo
    if event.new_chat_member.status not in ("member", "administrator", "creator"):
        return

    user = event.new_chat_member.user

    async with aiosqlite.connect(DATABASE) as db:

        # Verifica se o usuário já existe
        cursor = await db.execute(
            "SELECT id FROM usuarios WHERE id=?",
            (user.id,)
        )

        existe = await cursor.fetchone()

        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if existe:

            await db.execute("""
                UPDATE usuarios
                SET nome=?, username=?, ultima_vez=?
                WHERE id=?
            """, (
                user.full_name,
                user.username,
                agora,
                user.id
            ))

        else:

            await db.execute("""
                INSERT INTO usuarios
                (id,nome,username,primeira_vez,ultima_vez)
                VALUES(?,?,?,?,?)
            """, (
                user.id,
                user.full_name,
                user.username,
                agora,
                agora
            ))

        await db.execute("""
            INSERT INTO entradas
            (usuario_id,grupo_id,grupo_nome,data)
            VALUES(?,?,?,?)
        """, (
            user.id,
            event.chat.id,
            event.chat.title,
            agora
        ))

        await db.commit()

    print(f"Novo membro: {user.full_name} ({user.id})")


async def main():
    # Cria o banco caso não exista
    await iniciar_banco()

    print("🛡 Guardião iniciado com sucesso!")

    # Inicia o bot
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == "__main__":
    asyncio.run(main())
