import asyncio

from aiogram import executor, Bot, Dispatcher

from data.config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)

if __name__ == '__main__':
    from telegram_bot.TelegramBot import dp, send_to_admin

    executor.start_polling(dp, on_startup=send_to_admin)
