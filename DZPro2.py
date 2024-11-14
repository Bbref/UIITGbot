import asyncio
import nest_asyncio
from telegram.ext import Application
from dotenv import load_dotenv
import os
from datetime import datetime

# Разрешаем повторное использование текущего цикла событий
nest_asyncio.apply()

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.environ.get("TOKEN")


# Функция для обновления описания
async def update_description(app):
    while True:
        current_time = datetime.now().strftime("Время %H:%M")
        await app.bot.set_my_description(current_time)
        await asyncio.sleep(300)  # Обновление каждые 5 минут


# Основная функция
async def main():
    application = Application.builder().token(TOKEN).build()

    # Создаем задачу для обновления описания
    asyncio.create_task(update_description(application))

    # Запускаем polling
    await application.run_polling()


# Запуск приложения
if __name__ == "__main__":
    asyncio.run(main())
