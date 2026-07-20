import os
import asyncio
import aiosqlite

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime

from config import BOT_TOKEN, OWNER_IDS
from database import iniciar_banco


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


DATABASE = "guardiao.db"


@dp.message(Command("start"))
async def painel(message: Message):

    if message.from_user.id not in OWNER_IDS:
        return


    teclado = InlineKeyboardBuilder()

    teclado.button(
        text="👥 Novos Membros",
        callback_data="novos_membros"
    )

    teclado.adjust(1)


    await message.answer(
        "🛡 Guardião\n\nEscolha uma opção:",
        reply_markup=teclado.as_markup()
    )

@dp.chat_member()
async def novo_membro(event: ChatMemberUpdated):

    print("EVENTO CHAT_MEMBER RECEBIDO")

    if event.new_chat_member.status not in (
        "member",
        "administrator",
        "creator"
    ):
        return


    user = event.new_chat_member.user


    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            "SELECT id FROM usuarios WHERE id=?",
            (user.id,)
        )

        existe = await cursor.fetchone()


        agora = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )


        if existe:

            await db.execute("""
            UPDATE usuarios
            SET nome=?, username=?, ultima_vez=?
            WHERE id=?
            """,
            (
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
            """,
            (
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
        """,
        (
            user.id,
            event.chat.id,
            event.chat.title,
            agora
        ))


        await db.commit()


    print(
        f"Novo membro: {user.full_name} ({user.id})"
    )



async def main():

    await iniciar_banco()

    print("🛡 Guardião iniciado com sucesso!")


    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )



if __name__ == "__main__":
    asyncio.run(main())
