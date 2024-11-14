from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

async def start(update, context):
    keyboard = [['+', '-', '*', '/']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Введите два числа через пробел, затем выберите операцию:', reply_markup=reply_markup)

async def calculate(update, context):
    try:
        nums = update.message.text.split()
        if len(nums) != 2:
            raise ValueError
        num1, num2 = map(float, nums)
        context.user_data['nums'] = (num1, num2)
        await update.message.reply_text('Теперь выберите операцию:', reply_markup=ReplyKeyboardMarkup([['+', '-', '*', '/']], one_time_keyboard=True, resize_keyboard=True))
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите два числа через пробел.')

async def operation(update, context):
    op = update.message.text
    num1, num2 = context.user_data.get('nums', (None, None))
    if num1 is None or num2 is None:
        await update.message.reply_text('Сначала введите числа.')
        return
    result = None
    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == '*':
        result = num1 * num2
    elif op == '/':
        result = num1 / num2 if num2 != 0 else 'Ошибка: деление на ноль'
    await update.message.reply_text(f'Результат: {result}', reply_markup=ReplyKeyboardRemove())

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.Regex('^[+\\-*/]$'), calculate))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^[+\\-*/]$'), operation))
    application.run_polling()

if __name__ == "__main__":
    main()
