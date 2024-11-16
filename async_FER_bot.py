from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")

# URL вашего API
API_URL = "http://127.0.0.1:5000/analyze_sentiment"

# Команда /start
async def start(update, context):
    await update.message.reply_text("Привет! Отправь текст, и я определю его тональность!")

# Обработчик текстовых сообщений
async def analyze_text(update, context):
    text = update.message.text

    # Отправляем запрос к API
    try:
        response = requests.post(API_URL, json={'text': text})
        if response.status_code == 200:
            result = response.json()['result'][0]
            sentiment = result['label']
            score = result['score']
            await update.message.reply_text(f"Тональность: {sentiment}\nУверенность: {score:.2f}")
        else:
            await update.message.reply_text("Произошла ошибка при анализе текста.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

def main():
    # Создаем приложение Telegram-бота
    application = Application.builder().token(TOKEN).build()

    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))

    # Запуск
    application.run_polling()

if __name__ == "__main__":
    main()
