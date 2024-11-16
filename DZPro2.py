from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from fer import FER
import numpy as np
import os

# Загрузка переменных окружения из .env
load_dotenv()

# Загрузка токена бота
TOKEN = os.environ.get("TOKEN")

# Загрузка модели FER
detector = FER()

# Функция команды /start
async def start(update, context):
    await update.message.reply_text('Привет! Отправь этому боту фотографию лица человека для распознавания эмоции.')

# Функция обработки несжатых изображений
async def fer_document(update, context):
    await update.message.reply_text('Мы получили от тебя файл с фотографией. Идет распознавание эмоций...')

    # Извлекаем изображение в формате bytearray
    file = await update.message.document.get_file()
    image = await file.download_as_bytearray()

    # Переводим изображение в формат RGB
    img = np.asarray(Image.open(BytesIO(image)).convert('RGB'))

    # Выполняем предикт модели
    result = detector.detect_emotions(img)

    # Возвращаем результат обратно пользователю
    if result:
        emotions = result[0]['emotions']
        dominant_emotion = max(emotions, key=emotions.get)
        await update.message.reply_text(f"Доминирующая эмоция: {dominant_emotion}")
    else:
        await update.message.reply_text("Не удалось распознать лица на фотографии.")

# Функция обработки сжатых изображений
async def fer_photo(update, context):
    await update.message.reply_text('Мы получили от тебя фотографию. Идет распознавание эмоций...')

    # Извлекаем изображение в формате bytearray
    photo = await update.message.photo[-1].get_file()
    image = await photo.download_as_bytearray()

    # Переводим изображение в формат RGB
    img = np.asarray(Image.open(BytesIO(image)).convert('RGB'))

    # Выполняем предикт модели
    result = detector.detect_emotions(img)

    # Возвращаем результат обратно пользователю
    if result:
        emotions = result[0]['emotions']
        dominant_emotion = max(emotions, key=emotions.get)
        await update.message.reply_text(f"Доминирующая эмоция: {dominant_emotion}")
    else:
        await update.message.reply_text("Не удалось распознать лица на фотографии.")

def main():
    # Точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Добавляем обработчик несжатых фото
    application.add_handler(MessageHandler(filters.Document.IMAGE, fer_document))

    # Добавляем обработчик сжатых фото
    application.add_handler(MessageHandler(filters.PHOTO, fer_photo))

    # Запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()

if __name__ == "__main__":
    main()
