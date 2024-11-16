from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from fer import FER
import numpy as np
import cv2
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
    # Проверяем, содержит ли сообщение фотографию
    if not update.message.photo and not update.message.document:
        await update.message.reply_text('Пожалуйста, отправьте фотографию.')
        return

    await update.message.reply_text('Мы получили от тебя фотографию. Идет распознавание эмоций...')

    try:
        # Извлекаем файл (сжатая фотография или документ)
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
        elif update.message.document:
            file = await update.message.document.get_file()
        else:
            await update.message.reply_text('Не удалось обработать изображение.')
            return

        image = await file.download_as_bytearray()

        # Преобразуем изображение в RGB
        img = np.asarray(Image.open(BytesIO(image)).convert('RGB'))

        # Копируем изображение, чтобы оно было изменяемым
        img = img.copy()

        # Выполняем предикт модели
        result = detector.detect_emotions(img)

        if result:
            for face in result:
                box = face["box"]
                emotions = face["emotions"]
                dominant_emotion = max(emotions, key=emotions.get)

                # Преобразуем в формат BGR для корректной обработки OpenCV
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                # Рисуем рамку
                x, y, w, h = box
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Добавляем текст эмоции
                cv2.putText(
                    img,
                    f"{dominant_emotion}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

                # Конвертируем обратно в RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Преобразуем изображение обратно в формат BytesIO
            pil_image = Image.fromarray(img)
            buffer = BytesIO()
            pil_image.save(buffer, format="JPEG")
            buffer.seek(0)

            # Отправляем результат пользователю
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=buffer)
        else:
            await update.message.reply_text('Эмоции не распознаны.')

    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка при обработке изображения: {str(e)}')

def main():
    # Точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Добавляем обработчики фото (сжатые и документы)
    application.add_handler(MessageHandler(filters.PHOTO, fer))
    application.add_handler(MessageHandler(filters.Document.IMAGE, fer))

    # Запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()

if __name__ == "__main__":
    main()
