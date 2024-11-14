from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

async def start(update, context):
    await context.bot.set_my_description("Новое описание бота")
    print("Описание изменено")
    keyboard = [['Получить информацию о себе']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Нажмите на кнопку ниже:', reply_markup=reply_markup)

async def info(update, context):
    user = update.message.from_user
    await update.message.reply_text(f'ID: {user.id}\nUsername: {user.username}\nFirst Name: {user.first_name}')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^Получить информацию о себе$'), info))
    application.run_polling() #  <- Запускает цикл событий

if __name__ == "__main__":
    main() #  <-  Просто вызываем main()