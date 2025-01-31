from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from all_keyboards.inline_keyboards import start_keyboard

from create_bot import logger

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Рада Вас приветствовать, {message.from_user.first_name}!\n'
        )
    await message.answer(
        text='Выберите подходящий вариант',
        reply_markup=start_keyboard(message.from_user.id)
    )
