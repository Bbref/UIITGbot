from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
import os


# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN = os.environ.get("TOKEN")


# функция команды /start
async def start(update, context):
    await update.message.reply_text('Привет! Это самый простой бот.')


def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()