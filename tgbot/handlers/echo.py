from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


def alternate_case(string):
    return ''.join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(string))

async def bot_echo(message: types.Message):
    text = [
        f"Эхо...{message.text.upper()}...{alternate_case(message.text)}...{message.text.lower()}",
        "Лучше используй бота по назначению)",
        message.text
    ]

    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    if not message.text:
        return
    text = [
        f"Эхо...{message.text.upper()}...{alternate_case(message.text)}...{message.text.lower()}",
        "Лучше используй бота по назначению)"
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
