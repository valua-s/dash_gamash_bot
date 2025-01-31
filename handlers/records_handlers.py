from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from all_keyboards.inline_keyboards import payment_keyboard, accept_keyboard, cancel_keyboard, start_keyboard
from google_sheets_records.record_to_google_sheets import TableDashaRecorder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_bot import logger


class Record(StatesGroup):
    type = State()
    payment = State()


shop_router = Router()


@shop_router.callback_query(F.data == 'shop_assortiment')
async def shop_assortiment(call: CallbackQuery, state: FSMContext, bot: Bot):
    assortiment_dict: dict = {}
    record_maker: TableDashaRecorder = TableDashaRecorder()
    names_of_column = record_maker.worksheet.row_values(1)
    for name_of_column in names_of_column:
        cell = record_maker.worksheet.find(name_of_column)
        values_list = record_maker.worksheet.col_values(cell)
        assortiment_dict[name_of_column] = values_list
    # Сформировали словарь со всеми значениями {название колонки: [список всех значений]}
    
    for index in range(len(assortiment_dict.values())):
        await call.message.answer(
            text=(
                f'📦 Название товара: {assortiment_dict['Название'][index]}\n'
                ' \n'
                f'💰 Цена: {assortiment_dict['Стоимость'][index]}\n'
                ' \n'
                f'📝 Описание: {assortiment_dict['Описание'][index]}'
                  )
        )
        await bot.send_photo(
            call.message.chat_id,
            assortiment_dict['Ссылка на фото'][index]
            )
        