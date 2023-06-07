from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminMenu(InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_width = 1

    def add_button(self, text, callback_data):
        self.add(InlineKeyboardButton(text, callback_data=callback_data))

    def insert_button(self, text, callback_data):
        self.insert(InlineKeyboardButton(text, callback_data=callback_data))

    @property
    def row_width(self):
        return self._row_width

    @row_width.setter
    def row_width(self, count):
        self._row_width = count


async def get_admin_answer_menu(user_id, message):
    menu = AdminMenu()
    menu.add_button('Ответить пользователю', f'answer#{user_id}&{message}')

    return menu


async def get_contact_url():
    menu = InlineKeyboardMarkup()
    menu.add_button(
        'Контакт администратора',
        url="https://t.me/GelliToMellopy",
    )

    return menu
