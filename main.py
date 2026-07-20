import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import iniciar_banco

# Cria o bot
bot = Bot(token=BOT_TOKEN)

# Dispatcher
dp = Dispatcher()


async def main():
    # Cria o banco caso não exista
    await iniciar_banco()

    print("🛡 Guardião iniciado com sucesso!")

    # Inicia o bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
