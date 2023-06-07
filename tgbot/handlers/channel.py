import datetime
import os
from typing import Union

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tgbot import keyboards as kb, misc
from tgbot.validators import email_validator as email
from tgbot.models import models as db


async def send_posts_intern(message: Message):
    await message.answer(
        "",
        reply_markup=kb.main_menu,
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(send_posts_intern, commands=["/intern"], state=None)
