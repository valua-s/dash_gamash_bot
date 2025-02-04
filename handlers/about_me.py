from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message

about_me_router = Router()


@about_me_router.callback_query(F.data.contains('about_me'))
async def about_me(call: CallbackQuery, bot: Bot):
    await call.message.answer(
        text=(
        'Добрый день! Меня зовут Дарья Ганжурова и я делаю крутой продукт.\n\n'
        'Лёгкие гамаши для походов, трейлов и других активностей на пересечённой местности.\n'
        'Но, не только на гамашах держится этот мир:)))\n'
        'Поэтому в ассортименте появляются другие аксессуары, нужные туристу, альпинисту и трейлрайнеру\n'
        )
    )
    await call.message.answer(
        text=(
            'Как же купить?\n\n'
            'Варианты такие: \n'
            '1. Оформить заказ через этот бот и я свяжусь с Вами\n'
            '2. Написать мне в личные сообщения @DoraSiberianExplorer\n'
            '3. Написать комментарий к любому из сообщений в канале https://t.me/dora_siberian_explorer и я вам отвечу.'
        )
    )