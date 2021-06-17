from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

users_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Включить бота")],
        [KeyboardButton(text="Выключить бота")],
        ],
    resize_keyboard=True)

admin_keyboard = InlineKeyboardMarkup(row=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(
                                                  text='Список активных пользователей',
                                                  callback_data='get_active_users'
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text='Включить пользователя',
                                                  callback_data='activate_users'
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text='Выключить пользователя',
                                                  callback_data='deactivate_users'
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text='Включить бота',
                                                  callback_data='start_bot'
                                              ),
                                          ],
                                      ])

admin_callback = CallbackData("user", "name", 'chat_id', "mod")


def users_sheet_keyboard(users_sheet, mod):
    users = InlineKeyboardMarkup()
    if mod == 'on':
        for user in users_sheet:
            users.add(InlineKeyboardButton(
                text=users_sheet[user]['name'], callback_data=admin_callback.new(
                    name=users_sheet[user]['name'],
                    chat_id=user,
                    mod=mod)))

    if mod == 'off':
        for user in users_sheet:
            users.add(InlineKeyboardButton(text=users_sheet[user], callback_data=admin_callback.new(
                name=users_sheet[user], chat_id=user, mod=mod)))

    users.add(InlineKeyboardButton(text='Назад', callback_data='back_to_admin_keyboard'))

    return users
