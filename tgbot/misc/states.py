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
    main_menu = State()
    fill_form_again = State()
    fill_form_again_part2 = State()
    fill_form_again_part3 = State()
    fill_form_again_part4 = State()
    fill_form_again_part5 = State()
    fill_form_again_part6 = State()
    fill_form_over = State()
    support = State()
    supp_question = State()
    join_to_community = State()
    about_project = State()
    about_project2 = State()


class FSMAdmin(StatesGroup):
    admin_question = State()
    support_contact = State()
