import datetime
import os
from typing import Union

from aiogram import Dispatcher
from aiogram.types import (
    Message,
    CallbackQuery,
    PollAnswer,
    ChatMemberUpdated,
)
from aiogram.dispatcher import FSMContext

from tgbot import keyboards as kb, misc
from tgbot.validators import email_validator as email
from tgbot.models import models as db

last_message = None
last_error_email = ()


async def user_start(
    answr: Union[Message, CallbackQuery],
    state: FSMContext,
):
    user_tg_id = answr.from_user.id
    user = await db.get_user(user_tg_id)

    print(user)

    current_state = await state.get_state()
    print(current_state)

    if not user:
        await db.create_user(
            user_tg_id,
            answr.from_user.full_name,
            answr.from_user.username,
            datetime.datetime.now(),
        )

    elif str(current_state) in str(misc.states.FSMStart.main_menu):
        pass

    else:
        await main_menu(answr, state)
        return


    if type(answr) is Message and str(current_state) not in str(misc.states.FSMStart.main_menu):
        send = answr
        await send.reply(
            "Привет из цифрового пространства SmartConnectHub!🤖\n"
            "Давай познакомимся? Расскажи немного о себе!ℹ️"
        )
        await state.set_state(misc.states.FSMStart.handshake)

    elif type(answr) is CallbackQuery or type(answr) is Message:

        if type(answr) is Message:
            send = answr.reply

        else:
            send = answr.message.edit_text

        await send(
            "Хорошо! Давайте начнём с чистого листа.😌",
        )
        await state.set_state(misc.states.FSMStart.fill_form_again)


    if type(answr) is Message:
        send = answr
    else:
        send = answr.message

    await send.reply(
        "Какой у вас пол?",
        reply_markup=await kb.inline_user.get_inline_start_menu(),
    )


async def age_choice(
    callback: CallbackQuery,
    state: FSMContext,
    **kwargs,
):

    if callback.data in ("categories#male", "categories#female"):
        async with state.proxy() as data:
            data['sex'] = callback.data.split("#")[1]
            print(data)

    if "categories#" in callback.data:

        await callback.message.edit_text(
            "Выберите категорию",
            reply_markup=await kb.inline_user.get_inline_age_menu(
                callback.data,
            ),
        )

    else:

        await callback.message.edit_text(
            "Сколько Вам лет?",
            reply_markup=await kb.inline_user.get_inline_age_menu(
                callback.data,
            ),
        )

    current_state = await state.get_state()

    if str(current_state) in str(misc.states.FSMStart.handshake):
        await state.set_state(misc.states.FSMStart.age_choice)

    elif str(current_state) in str(misc.states.FSMStart.age_choice):
        pass

    else:
        await state.set_state(misc.states.FSMStart.fill_form_again_part2)
    print(f"---{current_state}")


async def choice_education(callback: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        age = callback.data.split('#')
        data['age'] = age[1]

    await callback.message.edit_text(
        "Где вы учитесь?",
        reply_markup=await kb.inline_user.get_education_menu(),
    )

    current_state = await state.get_state()
    if str(current_state) in str(misc.states.FSMStart.age_choice):
        await state.set_state(misc.states.FSMStart.education_choice)
    else:
        await state.set_state(misc.states.FSMStart.fill_form_again_part3)


async def choice_interest_category(callback: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        education = callback.data.split('#')
        print(education[1])
        data['education'] = education[1]

    await callback.message.edit_text(
        "Что Вас интересует?",
        reply_markup=await kb.inline_user.get_interest_menu(),
    )
    current_state = await state.get_state()
    if str(current_state) in str(misc.states.FSMStart.education_choice):
        await state.set_state(misc.states.FSMStart.interest_category_choice)
    else:
        await state.set_state(misc.states.FSMStart.fill_form_again_part4)


async def choice_experience(callback: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        category = callback.data.split('#')
        print(category[1])
        data['interest_category'] = category[1]

    await callback.message.edit_text(
        "Каков Ваш уровень знаний?",
        reply_markup=await kb.inline_user.get_experience_menu(),
    )

    current_state = await state.get_state()
    if str(current_state) in str(misc.states.FSMStart.interest_category_choice):
        await state.set_state(misc.states.FSMStart.experience_choice)
    else:
        await state.set_state(misc.states.FSMStart.fill_form_again_part5)


async def email_input(answr: Union[CallbackQuery, Message], state: FSMContext):

    global last_message

    if type(answr) is CallbackQuery:
        async with state.proxy() as data:
            experience = answr.data.split('#')
            print(experience[1])
            data['experience'] = experience[1]

        last_message = await answr.message.edit_text(
            "Пожалуйста, введите ваш email 📧\n\n"
            "В SmartConnect мы также не любим спам.\n"
            "Мы ценим ваш комфорт, поэтому будем отправлять "
            "вам только важную информацию!",
            reply_markup=await kb.inline_user.get_email_menu(),
        )
    else:
        global last_error_email
        await last_message.delete()
        last_error_email = last_error_email + (answr, )
        last_message = await answr.reply(
            "Пожалуйста, введите корректный email 📧",
            reply_markup=await kb.inline_user.get_email_menu(),
        )
    current_state = await state.get_state()
    if str(current_state) in str(misc.states.FSMStart.experience_choice):
        await state.set_state(misc.states.FSMStart.email)
    else:
        await state.set_state(misc.states.FSMStart.fill_form_again_part6)


async def showdown(answr: Union[CallbackQuery, Message], state: FSMContext):

    current_state = await state.get_state()

    if type(answr) is Message:
        validate_email = await email.validate_email(answr.text)
        if validate_email:
            async with state.proxy() as data:
                data['email'] = answr.text
        else:
            await state.set_state(misc.states.FSMStart.email_error)
            await email_input(answr, state)
            return

    data = await state.get_data()
    print(data)
    await db.update_user(
        answr.from_user.id,
        **data,
    )

    if (
        str(current_state) in str(misc.states.FSMStart.email) or
        str(current_state) in str(misc.states.FSMStart.about_project2) or
        str(current_state) in str(misc.states.FSMStart.introduce_part2) or
        str(current_state) in str(misc.states.FSMStart.the_path_part2)
    ):
        await state.set_state(misc.states.FSMStart.showdown)

    elif str(current_state) in str(misc.states.FSMStart.fill_form_again_part6):
        await state.set_state(misc.states.FSMStart.fill_form_over)
        await main_menu(answr, state)
        return

    msg = (
        f'Отлично, вот мы и познакомились, {answr.from_user.first_name}!🤝\n\n'
        'Спасибо за то, что заполнили нашу небольшую анкету. '
        'Мы рады приветствовать вас в нашем сообществе! 🌟\n\n'
        'Ваше участие поможет нам лучше понять '
        'ваши предпочтения и потребности. '
        'Мы стремимся создать для Вас окружение,'
        ' которое точно соответствовало Вашим интересам'
        'и приносило максимальную пользу. 💡\n\n'
        'Не стесняйтесь задавать вопросы или делиться своими мыслями с нами. '
        'Мы здесь, чтобы помочь Вам и обеспечить приятный опыт. 🤗\n\n'
        'Еще раз спасибо за ваше участие! '
        'Мы ценим Ваше время и доверие. '
        'Добро пожаловать в наше сообщество! 🎉\n\n'
        'Если у вас возникнут вопросы или нужна дополнительная информация, '
        'не стесняйтесь обращаться. Мы всегда готовы помочь! 💪\n\n'
        'С наилучшими пожеланиями, '
        'команда SmartConnectHub!'
    )
    if type(answr) is CallbackQuery:

        if answr.data == 'next#4!':
            await last_message.delete()
        elif answr.data == 'next#55':
            await last_message.delete()

        await answr.message.edit_text(
            text=msg,
            reply_markup=await kb.inline_user.get_showdown_menu(),
        )
    else:
        if last_message:
            await last_message.delete()
            await answr.delete()
            if last_error_email:
                for error_email in last_error_email:
                    await error_email.delete()
        await answr.answer(
            text=msg,
            reply_markup=await kb.inline_user.get_showdown_menu(),
        )

# -------------------------------Бот представляет себя------------------------


async def introduce_yourself_part1(callback: CallbackQuery, state: FSMContext):
    global last_message
    last_message = await callback.message.edit_text(
        "Привет! Я - Smart-Bot8000!🤖\n\n"
        "Моя задача - помогать в организации, "
        "обучении и управлении сообществами.🐝\n"
        "Я обладаю множеством умных возможностей "
        "и готов помочь вам во многих задачах.\n"
        "Для организаторов сообществ я являюсь настоящим помощником!\n"
        "Больше не нужно беспокоиться организацией оффлайн-встреч, "
        "поиском обучающих материалов или придумыванием задач "
        "и проектов для участников. "
        "Я возьму на себя эти задачи и сделаю все, "
        "чтобы ваше сообщество процветало.\n\n"
        "А для участников сообществ я предлагаю простое решение! "
        "Просто заполните небольшую анкету, и мои алгоритмы🖥 смогут "
        "определить наилучшее "
        "сообщество для вас.",
        reply_markup=await kb.inline_user.get_introduce_menu(1),
    )
    await state.set_state(misc.states.FSMStart.introduce_part1)


async def introduce_yourself_part2(callback: CallbackQuery, state: FSMContext):
    await last_message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "В таком сообществе Вы "
        "будете получать свежие обучающие материалы, "
        "участвовать в оффлайн-встречах и наслаждаться "
        "увлекательным общением.\n"
        "Не стесняйтесь обращаться ко мне, я готов помочь вам воплотить "
        "ваши идеи и сделать ваше сообщество настоящим местом роста и "
        "взаимодействия.\n\nДавайте вместе создадим что-то удивительное!✨",
        reply_markup=await kb.inline_user.get_introduce_menu(2),
    )
    await state.set_state(misc.states.FSMStart.introduce_part2)
# -------------------------------КОНЕЦ-----------------------------------------

# -------------------------------Бот рассказывает о том что происходит---------


async def show_the_path(callback: CallbackQuery, state: FSMContext):
    global last_message
    last_message = await callback.message.edit_text(
        "Как замечательно, что вы задали этот вопрос!"
        "\nЕсли вы действительно заинтересованы,"
        "то вы можете присоединиться к нашему "
        "удивительному сообществу прямо сейчас.\n"
        "Представьте только! У вас уже сейчас есть возможность общаться, "
        "создавать проекты и обучаться вместе с великолепными людьми!\n",
        reply_markup=await kb.inline_user.get_introduce_menu(3),
    )
    await state.set_state(misc.states.FSMStart.the_path)


async def show_the_path_part2(callback: CallbackQuery, state: FSMContext):
    await last_message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Если вам нужно время, если вы хотите отредактировать анкету или у вас "
        "есть какие-либо вопросы, не стесняйтесь перейти в "
        "главное меню, просто нажав 'Я ещё осмотрюсь здесь'!",
        reply_markup=await kb.inline_user.get_introduce_menu(4),
    )
    await state.set_state(misc.states.FSMStart.the_path_part2)

# -------------------------------КОНЕЦ-------------------------


async def main_menu(answr: Union[CallbackQuery, Message], state: FSMContext):
    current_state = await state.get_state()

    print(current_state)

    if str(current_state) in str(misc.states.FSMStart.fill_form_over):

        text_to_user = (
            "Анкету переделали, а что дальше делать будем?😏\n\n"
            "Да и неважно это, ведь с Вами лучший "
            "помощник в саморазвитии и творчестве - Smart-Bot8000🛠🦾"
        )

        if type(answr) is CallbackQuery:
            send = answr.message.edit_text
        else:
            send = answr.reply

    else:
        text_to_user = (
            "Добро пожаловать!🪬\n\n"
            "Лучший бот для саморазвития, "
            "творчества и организации сообществ!\n"
        )
        if type(answr) is CallbackQuery:
            send = answr.message.edit_text
        else:
            send = answr.reply

    await send(
        text=text_to_user,
        reply_markup=await kb.inline_user.get_main_menu(),
    )

    await state.set_state(misc.states.FSMStart.main_menu)


# Служба поддержки


async def support(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Если вы хотите обратиться к администратору, нажмите на кнопки ниже!",
        reply_markup=await kb.inline_user.get_support_menu(),
    )

    await state.set_state(misc.states.FSMStart.support)


async def supp_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вы можете задавать вопросы - "
        "на них обязательно ответит администратор!👨‍💻\n"
        "Если Вы хотите перейти обратно в меню, то пришлите 'Главная' "
        "отдельным сообщением✌️",
    )
    await state.set_state(misc.states.FSMStart.supp_question)


async def ask_to_admin(message: Message):
    await message.reply(
        "Спасибо за ваш вопрос!"
    )
    user_id = message.from_user.id
    await message.bot.send_message(
        chat_id=os.getenv("ADMIN_ID"),
        text=(
            f"Пришел вопрос от пользователя: {message.from_user.full_name}\n"
            f"ID пользователя {user_id}\n"
            f"Юзернейм: {message.from_user.username}\n\n"
            f"Сам вопрос:\n{message.text}"
        ),
        reply_markup=await kb.inline_admin.get_admin_answer_menu(
            user_id,
            message.text,
        ),
    )


async def support_contact(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вы можете связаться с администратором через телеграмм!👇",
        reply_markup=await kb.inline_admin.get_contact_url(),
    )
    await state.set_state(misc.states.FSMAdmin.support_contact)


async def join_to_community(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Сейчас мы отправляемся в мир нулей и единиц - Developers Hub!🖥\n"
        "Приятного путешествия!🛸\n\n"
        "*На данный момент прототип поддерживает "
        "только одно сообщество - сообщество разработчиков ПО.\n",
        reply_markup=await kb.inline_user.get_join_community_menu(),
    )
    await state.set_state(misc.states.FSMStart.join_to_community)


async def poll_answer(poll_answer: PollAnswer):
    # this handler starts after user choosed any answer

    answer_ids = poll_answer.option_ids # list of answers
    print(answer_ids)
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id
    print(poll_answer)
    print("fool")


async def on_chat_member_join(message: ChatMemberUpdated):
    # Проверяем, что событие связано с новым пользователем
    if message.new_chat_member.is_bot:
        return

    # Получаем информацию о пользователе
    user = message.new_chat_member.user
    first_name = user.first_name if user.first_name else ""
    last_name = user.last_name if user.last_name else ""

    # Формируем приветственное сообщение
    welcome_message = f"Привет, {first_name} {last_name}! Добро пожаловать в наш чат!"

    # Отправляем приветственное сообщение
    await message.reply_text(welcome_message)


async def about_project(callback: CallbackQuery, state: FSMContext):
    global last_message

    last_message = await callback.message.edit_text(
        "SmartConnectHub - интересный проект с хорошими перспективами.\n"
        "На данный момент этого всего лишь прототип, но по мере развития(а оно обязательно будет) "
        "будет добавлено множество полезных функций.",
        reply_markup=await kb.inline_user.get_introduce_menu(88),
    )
    await state.set_state(misc.states.FSMStart.about_project)


async def about_project2(callback: CallbackQuery, state: FSMContext):
    await last_message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Я отдельно задумался о внедрении исскуственного интеллекта в проект.\n"
        "Это был достаточно трудный вопрос, поскольку после изучения уже существующих инструментов было нелегко"
        " придумать что-то стоящее. К тому же я бэкенд-разработчик, но не специалист по ИИ.\n"
        "Я остановился на том, что нужно внедрить уже существующие модели GPT и Midjourney5 в чаты сообществ, "
        "а в самого бота уже потом интегрировать ИИ для распределения пользователей по сообществам.\n"
        "К слову я даже проводил онлайн и оффлайн опросы на эту тему и будущие пользователи были со мной согласны.\n"
        "Сейчас бот способен доставать полезные обучающие материалы с помощью Bing AI(ИИ от Microsoft) и постить их на канал сообщества каждые 24 часа.\n"
        "Так же бот может проводить опросы для оффлайн встреч.\n"
        "Я надеюсь что Вам понравилась моя задумка, ведь это главная награда для меня:)\n"
        "В любом случае я постарался найти применения своим инженерным навыкам "
        "в области программирования и проектирования информационных систем. "
        "бот полностью написан на Python.\n\n"
        "С наилучшими пожеланиями,\n"
        "разработчик SmartConnectHub Иван!",
        reply_markup=await kb.inline_user.get_introduce_menu(55),
    )
    await state.set_state(misc.states.FSMStart.about_project2)


def register_user(dp: Dispatcher):

    dp.register_callback_query_handler(
        user_start,
        lambda call: "fill_form_again" in call.data,
        state=misc.states.FSMStart.main_menu,
    )
    dp.register_message_handler(
        user_start,
        lambda message: message.text == "/start",
        state="*",
    )
    dp.register_callback_query_handler(
        age_choice,
        lambda call: "categories" in call.data or any(
            category in call.data for category in [
                "Inter",
                "Junior",
                "Middle",
                "Senior"
            ]
        ),
        state=[
            misc.states.FSMStart.handshake,
            misc.states.FSMStart.age_choice,
            misc.states.FSMStart.fill_form_again,
            misc.states.FSMStart.fill_form_again_part2
        ]
    )
    dp.register_callback_query_handler(
        choice_education,
        lambda call: call.data.startswith("age"),
        state=(
            misc.states.FSMStart.age_choice,
            misc.states.FSMStart.fill_form_again_part2,
        )
    )
    dp.register_callback_query_handler(
        choice_interest_category,
        lambda call: call.data.startswith("education"),
        state=(
            misc.states.FSMStart.education_choice,
            misc.states.FSMStart.fill_form_again_part3,
        )
    )
    dp.register_callback_query_handler(
        choice_experience,
        lambda call: "interest#" in call.data,
        state=(
            misc.states.FSMStart.interest_category_choice,
            misc.states.FSMStart.fill_form_again_part4,
        )
    )
    dp.register_callback_query_handler(
        email_input,
        lambda call: call.data.startswith("experience"),
        state=(
            misc.states.FSMStart.experience_choice,
            misc.states.FSMStart.email_error,
            misc.states.FSMStart.introduce_part1,
            misc.states.FSMStart.fill_form_again_part5,
        )
    )
    dp.register_callback_query_handler(
        showdown,
        lambda answr: answr.data.startswith("email_") or answr.data.startswith(
            "next#"
        ),
        state=(
            misc.states.FSMStart.email,
            misc.states.FSMStart.email_error,
            misc.states.FSMStart.introduce_part2,
            misc.states.FSMStart.the_path_part2,
            misc.states.FSMStart.fill_form_again_part6,
            misc.states.FSMStart.about_project2,
        )
    )
    dp.register_message_handler(
        showdown,
        state=(
            misc.states.FSMStart.email,
            misc.states.FSMStart.fill_form_again_part6,
        )
    )
    dp.register_callback_query_handler(
        introduce_yourself_part1,
        lambda call: "who_are_you" in call.data,
        state=misc.states.FSMStart.showdown,
    )
    dp.register_callback_query_handler(
        introduce_yourself_part2,
        lambda call: "next#1" in call.data,
        state=misc.states.FSMStart.introduce_part1,
    )
    dp.register_callback_query_handler(
        show_the_path,
        lambda call: "where_am_i" in call.data,
        state=misc.states.FSMStart.showdown,
    )
    dp.register_callback_query_handler(
        show_the_path_part2,
        lambda call: "next#3" in call.data,
        state=misc.states.FSMStart.the_path,
    )
    dp.register_callback_query_handler(
        main_menu,
        lambda call: "menu" in call.data or ("back" in call.data),
        state=(
            misc.states.FSMStart.showdown,
            misc.states.FSMStart.support,
        )
    )
    dp.register_message_handler(
        main_menu,
        state=misc.states.FSMStart.fill_form_over,
    )
    dp.register_message_handler(
        main_menu,
        lambda message: message.text == "Главная",
        state=misc.states.FSMStart.supp_question,
    )
    dp.register_callback_query_handler(
        support,
        lambda call: "support" in call.data,
        state=(
            misc.states.FSMStart.main_menu,
        )
    )
    dp.register_callback_query_handler(
        supp_question,
        lambda call: "ask" in call.data,
        state=misc.states.FSMStart.support,
    )
    dp.register_message_handler(
        ask_to_admin,
        state=misc.states.FSMStart.supp_question,
    )
    dp.register_callback_query_handler(
        support_contact,
        lambda call: "menu#supp" in call.data,
        state=misc.states.FSMStart.support,
    )
    dp.register_callback_query_handler(
        join_to_community,
        lambda call: "join_to_community" in call.data,
        state=(
            misc.states.FSMStart.main_menu,
            misc.states.FSMStart.showdown,
        )
    )
    dp.register_poll_answer_handler(
        poll_answer,
    )
    dp.register_chat_member_handler(
        on_chat_member_join
    )
    dp.register_callback_query_handler(
        about_project,
        lambda callback: "#about_project" in callback.data,
        state=misc.states.FSMStart.showdown
    )
    dp.register_callback_query_handler(
        about_project2,
        lambda callback: "88" in callback.data,
        state=misc.states.FSMStart.about_project
    )
