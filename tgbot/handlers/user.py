from typing import Union

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tgbot import keyboards as kb, misc
from tgbot.validators import email_validator as email

last_message = None
last_error_email = ()


async def user_start(message: Message, state: FSMContext):
    await message.reply(
        "Привет из цифрового пространства SmartConnectHub!🤖\n"
        "Давай познакомся? Расскажи немного о себе!ℹ️"
    )
    await message.answer(
        "Какой у вас пол?",
        reply_markup=await kb.inline_user.get_inline_start_menu(),
    )
    await state.set_state(misc.states.FSMStart.handshake)


async def sex_choice(
    callback: CallbackQuery,
    state: FSMContext,
    **kwargs,
):

    async with state.proxy() as data:
        data['sex'] = callback

    if callback.data in "categories":

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

    await state.set_state(misc.states.FSMStart.age_choice)


async def choice_education(callback: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        age = callback.data.split('#')
        print(age[1])
        data['age'] = age[1]

    await callback.message.edit_text(
        "Где вы учитесь?",
        reply_markup=await kb.inline_user.get_education_menu(),
    )

    await state.set_state(misc.states.FSMStart.education_choice)


async def choice_interest_category(callback: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        education = callback.data.split('#')
        print(education[1])
        data['education'] = education[1]

    await callback.message.edit_text(
        "Что Вас интересует?",
        reply_markup=await kb.inline_user.get_interest_menu(),
    )

    await state.set_state(misc.states.FSMStart.interest_category_choice)


async def choice_experience(callback: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        category = callback.data.split('#')
        print(category[1])
        data['interest_category'] = category[1]

    await callback.message.edit_text(
        "Каков Ваш уровень знаний?",
        reply_markup=await kb.inline_user.get_experience_menu(),
    )

    await state.set_state(misc.states.FSMStart.experience_choice)


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
            "Мы ценим ваш комфорт, поэтому будем отправлять"
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

    await state.set_state(misc.states.FSMStart.email)


async def showdown(answr: Union[CallbackQuery, Message], state: FSMContext):

    if type(answr) is Message:
        validate_email = await email.validate_email(answr.text)
        if validate_email:
            async with state.proxy() as data:
                data['email'] = answr.text
        else:
            await state.set_state(misc.states.FSMStart.email_error)
            await email_input(answr, state)
            return

    msg = (
        f'Отлично, вот мы и познакомились, {answr.from_user.first_name}!🤝\n\n'
        'Спасибо за то, что заполнили нашу небольшую анкету. '
        'Мы рады приветствовать вас в нашем сообществе! 🌟\n\n'
        'Ваше участие поможет нам лучше понять'
        'ваши предпочтения и потребности.'
        'Мы стремимся создать для Вас окружение,'
        ' которое точно соответствовало Вашим интересам'
        'и приносило максимальную пользу. 💡\n\n'
        'Не стесняйтесь задавать вопросы или делиться своими мыслями с нами.'
        'Мы здесь, чтобы помочь Вам и обеспечить приятный опыт. 🤗\n\n'
        'Еще раз спасибо за ваше участие!'
        'Мы ценим Ваше время и доверие.'
        'Добро пожаловать в наше сообщество! 🎉\n\n'
        'Если у вас возникнут вопросы или нужна дополнительная информация,'
        'не стесняйтесь обращаться. Мы всегда готовы помочь! 💪\n\n'
        'С наилучшими пожеланиями, '
        'команда SmartConnectHub!'
    )
    if type(answr) is CallbackQuery:

        if answr.data == 'next#4!':
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

    await state.set_state(misc.states.FSMStart.showdown)

# -------------------------------Бот представляет себя------------------------


async def introduce_yourself_part1(callback: CallbackQuery, state: FSMContext):
    global last_message
    last_message = await callback.message.edit_text(
        "Привет! Я - Smart-Bot8000!🤖\n\n"
        "Моя задача - помогать в организации,"
        "обучении и управлении сообществами.🐝\n"
        "Я обладаю множеством умных возможностей"
        "и готов помочь вам во многих задачах.\n"
        "Для организаторов сообществ я являюсь настоящим помощником!\n"
        "Больше не нужно беспокоиться организацией оффлайн-встреч,"
        "поиском обучающих материалов или придумыванием задач"
        "и проектов для участников."
        "Я возьму на себя эти задачи и сделаю все,"
        "чтобы ваше сообщество процветало.\n\n"
        "А для участников сообществ я предлагаю простое решение!"
        "Просто заполните небольшую анкету, и мои алгоритмы🖥 смогут"
        "определить наилучшее"
        "сообщество для вас.",
        reply_markup=await kb.inline_user.get_introduce_menu(1),
    )
    await state.set_state(misc.states.FSMStart.introduce_part1)


async def introduce_yourself_part2(callback: CallbackQuery, state: FSMContext):
    await last_message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "В таком сообществе Вы"
        "будете получать свежие обучающие материалы,"
        "участвовать в оффлайн-встречах и наслаждаться"
        "увлекательным общением.\n"
        "Не стесняйтесь обращаться ко мне, я готов помочь вам воплотить"
        "ваши идеи и сделать ваше сообщество настоящим местом роста и"
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
        "то вы можете присоединиться к нашему"
        "удивительному сообществу прямо сейчас.\n"
        "Представьте только! У вас уже сейчас есть возможность общаться,"
        "создавать проекты и обучаться вместе с великолепными людьми!\n",
        reply_markup=await kb.inline_user.get_introduce_menu(3),
    )
    await state.set_state(misc.states.FSMStart.the_path)


async def show_the_path_part2(callback: CallbackQuery, state: FSMContext):
    await last_message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Если вам нужно время, если вы хотите отредактировать анкету или у вас"
        "есть какие-либо вопросы, не стесняйтесь перейти в"
        "главное меню, просто нажав 'Я ещё осмотрюсь здесь'!",
        reply_markup=await kb.inline_user.get_introduce_menu(4),
    )
    await state.set_state(misc.states.FSMStart.the_path_part2)

# -------------------------------КОНЕЦ-------------------------


async def main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Добро пожаловать!🪬\n\n"
        "Лучший бот для организации, обучения и управления сообществами!\n",
        reply_markup=await kb.inline_user.get_main_menu(),
    )
    await state.set_state(misc.states.FSMStart.main_menu)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(
        sex_choice,
        lambda call: "back" in call.data or "categories" in call.data or any(
            category in call.data for category in [
                "Inter",
                "Junior",
                "Middle",
                "Senior"
            ]
        ),
        state=[misc.states.FSMStart.handshake, misc.states.FSMStart.age_choice]
    )
    dp.register_callback_query_handler(
        choice_education,
        lambda call: call.data.startswith("age"),
        state=misc.states.FSMStart.age_choice,
    )
    dp.register_callback_query_handler(
        choice_interest_category,
        lambda call: call.data.startswith("education"),
        state=misc.states.FSMStart.education_choice,
    )
    dp.register_callback_query_handler(
        choice_experience,
        lambda call: "interest#" in call.data,
        state=misc.states.FSMStart.interest_category_choice,
    )
    dp.register_callback_query_handler(
        email_input,
        lambda call: call.data.startswith("experience"),
        state=(
            misc.states.FSMStart.experience_choice,
            misc.states.FSMStart.email_error,
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
        )
    )
    dp.register_message_handler(
        showdown,
        state=misc.states.FSMStart.email,
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
        lambda call: "menu" in call.data,
        state=misc.states.FSMStart.showdown,
    )
