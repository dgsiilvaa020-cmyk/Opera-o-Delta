import os
import asyncio
import aiosqlite

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
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


@dp.callback_query(F.data == "novos_membros")
async def novos_membros(callback: CallbackQuery):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT 
                usuarios.nome,
                usuarios.username,
                usuarios.id,
                entradas.grupo_nome,
                entradas.data

            FROM entradas

            INNER JOIN usuarios
            ON usuarios.id = entradas.usuario_id

            ORDER BY entradas.id DESC

            LIMIT 10
        """)

        registros = await cursor.fetchall()


    if not registros:

        await callback.message.edit_text(
            "👥 Novos Membros\n\nNenhuma entrada registrada."
        )

        await callback.answer()
        return


    texto = "👥 Últimos membros:\n\n"


    for nome, username, usuario_id, grupo, data in registros:

        texto += (
            f"👤 {nome}\n"
            f"📛 @{username if username else 'sem @'}\n"
            f"🆔 {usuario_id}\n"
            f"👥 {grupo}\n"
            f"📅 {data}\n\n"
        )


    await callback.message.edit_text(texto)

    await callback.answer()
    

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
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    async with aiosqlite.connect(DATABASE) as db:

        # Procura o usuário
        cursor = await db.execute("""
            SELECT nome, username
            FROM usuarios
            WHERE id=?
        """, (user.id,))

        dados_usuario = await cursor.fetchone()

        if dados_usuario:

            nome_antigo, username_antigo = dados_usuario

            # Se mudou o nome
            if nome_antigo != user.full_name:

                await db.execute("""
                    INSERT INTO historico_nomes
                    (usuario_id, nome, data)
                    VALUES (?, ?, ?)
                """, (
                    user.id,
                    user.username,
                    agora
                ))

            # Se mudou o username
            if username_antigo != user.username:

                await db.execute("""
                    INSERT INTO historico_nomes
                    (usuario_id, nome, data)
                    VALUES (?, ?, ?)
                """, (
                    user.id,
                    user.username,
                    agora
                ))

            # Atualiza o cadastro
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

            # Primeiro cadastro
            await db.execute("""
                INSERT INTO usuarios
                (id, nome, username, primeira_vez, ultima_vez)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user.id,
                user.full_name,
                user.username,
                agora,
                agora
            ))

            # Salva o primeiro nome no histórico
            await db.execute("""
                INSERT INTO historico_nomes
                (usuario_id, nome, data)
                VALUES (?, ?, ?)
            """, (
                user.id,
                user.full_name,
                agora
            ))

            # Salva o primeiro username no histórico
            await db.execute("""
               INSERT INTO historico_usernames
               (usuario_id, username, data)
               VALUES (?, ?, ?)
            """, (
                user.id,
                user.username,
                agora
            ))

        # Registra a entrada no grupo
        await db.execute("""
            INSERT INTO entradas
            (usuario_id, grupo_id, grupo_nome, data)
            VALUES (?, ?, ?, ?)
        """, (
            user.id,
            event.chat.id,
            event.chat.title,
            agora
        ))

        await db.commit()

    print(f"Novo membro: {user.full_name} ({user.id})")


async def main():

    await iniciar_banco()

    print("🛡 Guardião iniciado com sucesso!")


    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )



if __name__ == "__main__":
    asyncio.run(main())
