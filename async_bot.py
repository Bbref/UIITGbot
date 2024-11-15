from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv
import os
import asyncio

# Загрузка переменных окружения из .env
load_dotenv()

# Загрузка токена бота
TOKEN = os.environ.get("TOKEN")

# Функция команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(5)
    await update.message.reply_text('Первая проверка')

# Функция команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Вторая проверка')

# Обработчик фотографий
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Замираем на 10 секунд
    await asyncio.sleep(10)

    # Отправляем сообщение пользователю
    await update.message.reply_text("Фотография получена в асинхронном режиме.")

def main():
    # Точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start, block=False))
    application.add_handler(CommandHandler("help", help_command, block=False))

    # Добавляем обработчик изображений
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
