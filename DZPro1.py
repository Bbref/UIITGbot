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


# Функция обработки изображений
async def fer(update, context):
    # Отправляем сообщение и сохраняем его, чтобы потом изменить
    processing_message = await update.message.reply_text('Мы получили от тебя фотографию. Идет распознавание эмоций...')

    try:
        # Извлекаем изображение в формате bytearray
        file = await update.message.document.get_file()
        image = await file.download_as_bytearray()

        # Переводим изображение в формат RGB
        img = np.asarray(Image.open(BytesIO(image)).convert('RGB'))

        # Выполняем предикт модели
        result = detector.detect_emotions(img)

        # Определяем доминирующую эмоцию
        if result:
            emotions = result[0]['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            emotion_text = f"Доминирующая эмоция: {dominant_emotion} ({emotions[dominant_emotion]:.2f})"
        else:
            emotion_text = "Не удалось распознать лица на фотографии."

    except Exception as e:
        emotion_text = f"Ошибка обработки изображения: {str(e)}"

    # Изменяем текст предыдущего сообщения
    await processing_message.edit_text('Мы получили от тебя фотографию. Эмоции распознаны.')

    # Отправляем результат обратно пользователю
    await update.message.reply_text(emotion_text)


def main():
    # Точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Добавляем обработчик изображений
    application.add_handler(MessageHandler(filters.Document.IMAGE, fer))

    # Запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()
