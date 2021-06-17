import asyncio
import random

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, BotCommand
from data.config import admin_id, active_users, users_data, initial_url, save_data
from initiator import dp, bot
from leads_creator.Leads_Downloader import download_from_forms, start_webdriver
from leads_creator.Leads_Sheet_Creator import leads_sheet_creator
from telegram_bot.keyboard import users_keyboard, admin_keyboard, users_sheet_keyboard, admin_callback


async def send_to_admin(dp):
    # Сообщает админу, что бот запущен
    await bot.send_message(chat_id=admin_id, text='Бот запущен, мой капитан')


@dp.message_handler(Command('start'), user_id=admin_id)
async def show_admin_keyboard(message: Message):
    await message.answer(text='Ваш штурвал, милорд', reply_markup=admin_keyboard)


@dp.message_handler(Command('start'))
async def show_admin_keyboard(message: Message):
    if f"{message.chat.id}" in users_data:
        await message.answer(
            text=f'Здравствуйте, {users_data[f"{message.chat.id}"]["name"]}!', reply_markup=users_keyboard)


@dp.callback_query_handler(text='start_bot', user_id=admin_id)
async def start_bot(call: CallbackQuery):
    driver = start_webdriver(initial_url)

    # Запускает бесконечный цикл отправления лидов по всем активным клиентам
    while True:
        for chat_id in active_users:
            number_of_downloads, users_data[f"{chat_id}"]['number_of_leads'] = download_from_forms(
                users_data[f"{chat_id}"]['page_name'],
                users_data[f"{chat_id}"]['number_of_leads'], driver)

            for number in range(1, number_of_downloads + 1):
                await bot.send_message(chat_id=chat_id, text=leads_sheet_creator())
        save_data(users_data, active_users)


        await asyncio.sleep(random.randint(1600, 2100))


@dp.callback_query_handler(text='get_active_users')
async def show_active_users(call: CallbackQuery):
    await call.answer('Список активных пользователей:\n\n' + ', '.join(active_users.values()), show_alert=True)


@dp.callback_query_handler(text='activate_users')
async def show_active_users(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=users_sheet_keyboard(users_data, mod='on'))


@dp.callback_query_handler(text='deactivate_users')
async def show_active_users(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=users_sheet_keyboard(active_users, mod='off'))


@dp.callback_query_handler(text='back_to_admin_keyboard')
async def show_active_users(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=admin_keyboard)


@dp.callback_query_handler(admin_callback.filter())
async def show_active_users(call: CallbackQuery, callback_data: dict):
    if callback_data.get('mod') == 'on':
        if f"{callback_data.get('chat_id')}" not in active_users:
            active_users[f"{callback_data.get('chat_id')}"] = callback_data.get('name')
            await call.answer(f'Пользователь {callback_data.get("name")} был включён', show_alert=True)
        else:
            await call.answer(f'Пользователь {callback_data.get("name")} уже включён', show_alert=True)

    if callback_data.get('mod') == 'off':
        if f"{callback_data.get('chat_id')}" in active_users:
            del active_users[f"{callback_data.get('chat_id')}"]
            await call.answer(f'Пользователь {callback_data.get("name")} был выключен', show_alert=True)
        else:
            await call.answer(f'Пользователь {callback_data.get("name")} уже включён', show_alert=True)

    save_data(users_data, active_users)


@dp.message_handler(text="11", user_id=admin_id)
async def send_active_users(message: Message):
    await message.answer(text=f'{active_users.values()}')


@dp.message_handler(text="Включить бота")
async def activator(message: Message):
    if f"{message.chat.id}" in users_data or f"{message.chat.id}" == admin_id:
        if f"{message.chat.id}" not in active_users:
            active_users[f"{message.chat.id}"] = users_data[f"{message.chat.id}"]['name']
        await message.answer(text='Автоматическая отправка заявок включена')
        await bot.send_message(chat_id=admin_id, text=f'{users_data[f"{message.chat.id}"]["name"]} включила бота')


@dp.message_handler(text="Выключить бота")
async def deactivator(message: Message):
    if f"{message.chat.id}" in users_data:
        if f"{message.chat.id}" in active_users:
            del active_users[f"{message.chat.id}"]
        await message.answer(text='Автоматическая отправка заявок выключена')
        await bot.send_message(chat_id=admin_id, text=f'{users_data[f"{message.chat.id}"]["name"]} выключила бота')


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand('start', 'Старт')
    ])
