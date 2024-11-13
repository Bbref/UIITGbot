from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os


# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN = os.environ.get("TOKEN")


# функция команды /start
async def start(update, context):
    await update.message.reply_text('Привет! При помощи этого бота мы будем сохранять файлы."')


# функция для изображений
async def image(update, context):
    await update.message.reply_text('Эй! Мы получили от тебя фотографию!')

    # достаем файл изображения из сообщения
    file = await update.message.photo[-1].get_file()
    
    # сохраняем изображение на диск
    # await file.download_to_drive("image.jpg")


# функция для видео
async def video(update, context):
    await update.message.reply_text('Эй! Мы получили от тебя видео!')

    # достаем видеофайл
    new_file = await update.message.video.get_file()

    # получаем имя файла
    video_name = update.message.video.file_name

    # сохраняем видео на диск
    await new_file.download_to_drive(video_name)


# функция для голосовых сообщений
async def voice(update, context):
    await update.message.reply_text('Эй! Мы получили от тебя голосовое сообщение!')

    # достаем аудиофайл
    new_file = await update.message.voice.get_file()

    # сохраняем видео на диск
    await new_file.download_to_drive('voice.mp3')


def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик сообщений с изображением
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик сообщений с видео
    application.add_handler(MessageHandler(filters.VIDEO, video))

    # добавляем обработчик сообщений с аудио
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()