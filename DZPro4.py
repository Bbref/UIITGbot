from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

async def capitalized_text(update, context):
    await update.message.reply_text('Сообщение начинается с большой буквы')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^[А-ЯA-Z]'), capitalized_text))
    application.run_polling()

if __name__ == "__main__":
    main()
