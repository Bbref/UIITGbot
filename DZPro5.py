from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

async def voice_duration(update, context):
    duration = update.message.voice.duration
    await update.message.reply_text(f'Длина голосового сообщения {duration} секунд')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.VOICE, voice_duration))
    application.run_polling()

if __name__ == "__main__":
    main()
