from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Указываем язык (например, "ru")
        language_code = "ru"

        current_description = await context.bot.get_my_description(language_code=language_code)
        current_short_description = await context.bot.get_my_short_description(language_code=language_code)

        print(f"Текущее описание: {current_description}")
        print(f"Текущее краткое описание: {current_short_description}")

        await context.bot.set_my_description("Новое описание", language_code=language_code)
        await context.bot.set_my_short_description("Новое короткое описание", language_code=language_code)

        new_description = await context.bot.get_my_description(language_code=language_code)
        new_short_description = await context.bot.get_my_short_description(language_code=language_code)

        print(f"Новое описание: {new_description}")
        print(f"Новое краткое описание: {new_short_description}")

        await update.message.reply_text("Описание и краткое описание бота изменены.")

    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text(f"Произошла ошибка: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()