
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import message
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '5801898411:AAGPgHbrHrMx-wABdJvEf_Dw7Qgb1EWZqCU'

# Инициализация бота и диспетчера
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Сообщение о начале работы бота
    """
    await message.reply("Добро пожаловать! Этот бот поможет вам в использовании калькулятора. "
                        "Чтобы использовать калькулятор, отправьте сообщение, содержащее математическое выражение.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    Сообщение с инструкцией по использованию бота
    """
    await message.reply("Этот бот является калькулятором. Отправьте сообщение, содержащее математическое выражение, "
                        "и бот вернет его результат. Все операции выполняются по порядку приоритетов.")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def evaluate_expression(message: types.Message):
    """
    Обработка математического выражения
    """
    expression = message.text
    try:
        result = eval(expression)
        await message.reply(f"**Выражение:** `{expression}`\n**Результат:** `{result}`", parse_mode=ParseMode.MARKDOWN)
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        await message.reply("Не удалось вычислить выражение. Проверьте правильность ввода.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
