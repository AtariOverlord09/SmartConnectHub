from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from tgbot.misc import states as st

user_id = None
msg = []


async def admin_start(message: Message):
    await message.reply("Здравствуйте, дорогой администратор!")


async def admin_input(callback: CallbackQuery, state: FSMContext):
    global user_id
    global msg
    user_id = callback.data.split("#")[1]
    msg.append(callback.data.split("&")[1])
    await callback.message.reply("Введите сообщение для пользователя: ")
    await state.set_state(st.FSMAdmin.admin_question)


async def admin_answer(message: Message):
    global msg

    text_to_user = (
        "Пришло сообщение от администратора на Ваш вопрос!\n"
        f"Ваш вопрос:\n{msg[0]}\n\n"
        f"Ответ администратора:\n{message.text}"
    )
    msg.pop(0) 
    msg = msg[1:]

    await message.reply("Сообщение отправленно!")
    await message.bot.send_message(
        user_id,
        text=text_to_user
    )


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_callback_query_handler(admin_input, lambda call: call.data.startswith("answer#"), state="*")
    dp.register_message_handler(admin_answer, state=st.FSMAdmin.admin_question)
