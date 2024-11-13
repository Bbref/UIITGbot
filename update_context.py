from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import time
import os


# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN = os.environ.get("TOKEN")


# функция команды /start
async def start(update, context):
    await update.message.reply_text('Привет! Это самый простой бот.')


# функция для текстовых сообщений
async def text(update, context):
    
    # использование update
    print(update)
    print()
    print(update.message.text)
    print(update.message.message_id)
    print(update.message.date)
    print(update.message.from_user.first_name)
    print(update.message.from_user.id)
    print()

    my_message = await update.message.reply_text(f'Получено текстовое сообщение: {update.message.text}')

    # использованеи context
    # time.sleep(5)
    # удаление сообщений
    # await context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=my_message.message_id)

    # закрепление сообщений
    # await context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    # изменение описания бота
    # await context.bot.set_my_short_description("Этот бот очень умный, добрый и красивый")



def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()