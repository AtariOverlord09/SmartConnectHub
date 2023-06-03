from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FirstStartMenu(InlineKeyboardMarkup):
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


async def get_inline_start_menu():
    menu = FirstStartMenu()
    menu.add_button('Мужской🤵‍♂️', 'categories#male')
    menu.add_button('Женский👩', 'categories#female')
    return menu


async def get_inline_age_menu(callback):
    menu = FirstStartMenu()

    print(callback)

    if "categories" in callback or "male" in callback or "female" in callback:

        menu.row_width = 2
        menu.insert_button('👨‍🦲Intern(16-20)', "Intern")
        menu.insert_button('🤵‍♂️Junior(21-29)', "Junior")
        menu.insert_button('👨‍🦰Middle(30-55)', "Middle")
        menu.insert_button('🧔Senior(56-100)', "Senior")

    else:

        menu.row_width = 5

        if "Intern" in callback:
            for age in range(16, 21):
                emoji = '👨‍🦲'
                menu.insert_button(f'{emoji}{age}', f'age#{age}')

        if "Junior" in callback:
            for age in range(21, 30):
                emoji = '🤵‍♂️'
                menu.insert_button(f'{emoji}{age}', f'age#{age}')

        if "Middle" in callback:
            for age in range(30, 56):
                emoji = '👨‍🦰'
                menu.insert_button(f'{emoji}{age}', f'age#{age}')

        if "Senior" in callback:
            for age in range(56, 101):
                emoji = '🧔'
                menu.insert_button(f'{emoji}{age}', f'age#{age}')

        menu.add_button('Вернуться назад', 'categories')

    return menu


async def get_age_categories():
    menu = FirstStartMenu()
    menu.row_width = 2


async def get_education_menu():
    menu = FirstStartMenu()

    menu.add_button('Я преподователь👨‍🏫', 'education#teacher')
    menu.add_button('Учусь в школе💼', 'education#shool')
    menu.add_button('Учусь в коллдже👨‍💻', 'education#college')
    menu.add_button('Учусь в университете👨‍🎓', 'education#university')
    menu.add_button('Нигде не учусь🌝', 'education#none')

    return menu


async def get_interest_menu():
    menu = FirstStartMenu()

    menu.add_button('Программирование и IT🧑‍💻🦾', 'interest#programming_and_it')
    menu.add_button('Дизайн🧑‍🎨', 'interest#design')
    menu.add_button('Музыка🎧', 'interest#music')
    menu.add_button('Рисование🎨🖌', 'interest#drawing')
    menu.add_button('Спорт и здоровье💪🥇', 'interest#sport_and_health')
    menu.add_button('Развитие🧘‍♂️', 'interest#development')
    menu.add_button('Предпринимательство💸💼', 'interest#business')

    return menu


async def get_experience_menu():
    menu = FirstStartMenu()
    menu.row_width = 11

    menu.insert_button('0', 'experience#0')
    menu.insert_button('1', 'experience#1')
    menu.insert_button('2', 'experience#2')
    menu.insert_button('3', 'experience#3')
    menu.insert_button('4', 'experience#4')
    menu.insert_button('5', 'experience#5')
    menu.insert_button('6', 'experience#6')
    menu.insert_button('7', 'experience#7')
    menu.insert_button('8', 'experience#8')
    menu.insert_button('9', 'experience#9')
    menu.insert_button('10', 'experience#10')

    return menu


async def get_email_menu():
    menu = FirstStartMenu()

    menu.add_button('Пропустить', 'email_skip')

    return menu


async def get_showdown_menu():
    menu = FirstStartMenu()

    menu.add_button('Так, стоп, ещё раз кто ты?😯', 'showdown#who_are_you')
    menu.add_button('Что происходит⁉️', 'showdown#where_am_i')
    menu.add_button('Я еще осмотрюсь здесь...👀', 'showdown#menu')
    menu.add_button('Я готов присоединиться к сообществу!😉', 'showdown#go!')

    return menu


async def get_introduce_menu(part):

    menu = FirstStartMenu()
    menu.add_button('Далее', f'next#{part}!')

    return menu


async def get_main_menu():
    menu = FirstStartMenu()

    menu.add_button('Присоединиться к сообществу!', 'menu#join_to_community')
    menu.add_button('Заполнить анкету заново', 'monitoring')
    menu.add_button('Служба поддержки', 'statistics')

    return menu
