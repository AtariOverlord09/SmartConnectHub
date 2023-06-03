from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMStart(StatesGroup):
    handshake = State()
    age_choice = State()
    education_choice = State()
    interest_category_choice = State()
    experience_choice = State()
    email = State()
    email_error = State()
    showdown = State()
    introduce_part1 = State()
    introduce_part2 = State()
    the_path = State()
    the_path_part2 = State()
