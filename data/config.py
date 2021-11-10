import json

BOT_TOKEN = 'bot_token' # Ввести токен бота
admin_id = 'admin_id' # Ввести айди админа
browser = 'browser' # Ввести полный путь до используемого браузера
initial_url = 'initial_url' # Ввести ссылку страницы со списком рекламных аккаунтов

with open('data/users_data.json', 'r', encoding='utf-8') as f:
    users_data = json.load(f)

with open('data/active_users.json', 'r', encoding='utf-8') as f:
    active_users = json.load(f)


def save_data(users_data, active_users):
    # Сохраняет данные текущие данные клиентов в словари
    with open('data/users_data.json', 'w', encoding='utf-8') as f:
        f.write(f'{json.dumps(users_data, ensure_ascii=False, indent=4)}')

    with open('data/active_users.json', 'w', encoding='utf-8') as f:
        f.write(f'{json.dumps(active_users, ensure_ascii=False, indent=4)}')
