from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Загружаем токен бота
TOKEN = os.environ.get("TOKEN")

# Создадим папку для сохранения изображений, если ее нет
os.makedirs('images', exist_ok=True)

# Задача 1: Функция команды /start
async def start(update, context):
    await update.message.reply_text('Первая задача выполнена')

# Задача 2: Функция для текстовых сообщений
async def text(update, context):
    words_count = len(update.message.text.split())
    await update.message.reply_text(f'Количество слов: {words_count}')

# Задача 3: Функция для голосовых сообщений
async def voice(update, context):
    await update.message.reply_text(f'ID голосового сообщения: {update.message.message_id}')

# Задача 4: Функция команды /warcraft
async def warcraft(update, context):
    keyboard = [['Альянс', 'Орда']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Выберите фракцию:', reply_markup=reply_markup)

# Обработчик нажатия кнопки "Альянс" или "Орда"
async def button_response(update, context):
    response_text = update.message.text
    await update.message.reply_text(f'Вы выбрали: {response_text}', reply_markup=ReplyKeyboardRemove())

# Задача 5: Функция для изображений
# функция для обработки изображений
async def image(update, context):
    photo = update.message.photo[-1]  # берем самое высокое качество изображения
    photo_id = update.message.message_id
    photo_path = f'images/{photo_id}.jpg'

    # Получаем файл изображения и скачиваем его
    file = await photo.get_file()
    await file.download_to_drive(photo_path)

    await update.message.reply_text(f'Изображение сохранено как {photo_path}')


def main():
    # Точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    application.add_handler(MessageHandler(filters.VOICE, voice))
    application.add_handler(CommandHandler("warcraft", warcraft))
    application.add_handler(MessageHandler(filters.PHOTO, image))
    application.add_handler(MessageHandler(filters.TEXT & (filters.Regex('^(Альянс|Орда)$')), button_response))

    # Запуск приложения
    application.run_polling()

if __name__ == "__main__":
    main()
