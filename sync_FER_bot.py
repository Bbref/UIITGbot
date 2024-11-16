from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from fer import FER
import numpy as np
import os


# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN = os.environ.get("TOKEN")

# загружаем модель FER
detector = FER()


# функция команды /start
async def start(update, context):
    await update.message.reply_text('Привет! Отправь этому боту фотографию лица человека для распознавания эмоции.')


# функция обработки изображений
async def fer(update, context):
    await update.message.reply_text('Мы получили от тебя фотографию. Идет распознавание эмоций...')
    
    # извлекаем изображение в формате bytearray
    file = await update.message.document.get_file()
    image = await file.download_as_bytearray()

    # переводим изображение в формат RGB
    img = np.asarray(Image.open(BytesIO(image)).convert('RGB'))

    # выполняем предикт модели
    result = detector.detect_emotions(img)

    # возвращаем результат обратно пользователю
    await update.message.reply_text(result[0]['emotions'])


def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик фото
    application.add_handler(MessageHandler(filters.Document.IMAGE, fer))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()