import math
import re
from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from all_keyboards.inline_keyboards import under_item_keyboard, \
    show_next_page, under_want_buy_keyboard, two_to_five_keyboard, \
    pay_order_keyboard, choose_logistic_keyboard, share_contact_keyboard, \
    logistic_keyboard
from google_sheets_records.record_to_google_sheets import TableDashaRecorder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_bot import logger
from db_handler.db_info import DB



class Item(StatesGroup):
    id_item = State()
    shop_dict = State()
    page = State()
    pages = State()
    cart = State()
    cart_for_dasha = State()
    fio = State()
    adress = State()
    phone = State()
    logistic = State()


shop_router = Router()

COUNT_OF_ITEMS_PER_PAGE = 5


@shop_router.callback_query(F.data.contains('shop_assortiment'))
async def shop_assortiment(call: CallbackQuery, state: FSMContext, bot: Bot):
    
    page = int(call.data.split(': ')[1])
    if page == 1:
        await call.message.answer('Один момент, уточню у Даши ассортимент :)')
        assortiment = await DB().get_queryset_of_count()
        await state.update_data(shop_dict=assortiment)
        await state.update_data(pages=math.ceil(len(assortiment)/COUNT_OF_ITEMS_PER_PAGE))
    else:
        await call.message.delete()
    await send_assortiment_page(call, state, page)


async def send_assortiment_page(call: CallbackQuery, state: FSMContext, page=1) -> None:
    
    data = await state.get_data()
    assortiment_dict = data.get('shop_dict')
    end_of_range = min(page * COUNT_OF_ITEMS_PER_PAGE, len(assortiment_dict))
    
    for index in range((page-1) * COUNT_OF_ITEMS_PER_PAGE, end_of_range): # Выводим список из COUNT_OF_ITEMS_PER_PAGE товаров
        id_item = assortiment_dict[index]['id']
        name = assortiment_dict[index]['name']
        cost = assortiment_dict[index]['amount']
        description = assortiment_dict[index]['description']
        await call.message.answer_photo(
            photo=assortiment_dict[index]['photo_link'],
            caption=(
                f'📦 Название товара: {name}\n'
                ' \n'
                f'💰 Цена: {cost} рублей\n'
                ' \n'
                f'📝 Описание: {description}'
                  ),
            reply_markup=under_item_keyboard(id_item, call.message.message_id)
        )
        
    if page < int(data.get('pages')): # если страница меньше общего числа страниц то формируем кнопку следующая страница
        await call.message.answer(
            f'Здесь только {COUNT_OF_ITEMS_PER_PAGE} товаров, показать еще?',
            reply_markup=show_next_page(page)
        )


@shop_router.callback_query(F.data.contains('item_id:'))
async def want_buy(call: CallbackQuery, bot: Bot, state: FSMContext):
    _, item_id, message_id = call.data.split(': ')
    
    data = await state.get_data()
    assortiment_dict = data.get('shop_dict')
    for item in assortiment_dict:
        if item.get('id') == int(item_id):
            item_name = item.get('name')
            item_price = item.get('amount')
    
    data = await state.get_data()
    full_cart = data.get('cart')
    if not full_cart:
        full_cart = {}
    full_cart[item_id] = [item_name, item_price, 1]
    
    await state.update_data(cart=full_cart)
    
    await call.message.answer(
        text=(f'Товар: {item_name} - стоимостью: {item_price} рублей\n'
              '\nДобавлен в корзину\n'
              '\n'
              'Вы можете:\n'
              '\n'
              ' - Cформировать корзину\n'
              ' - Изменить количество товара\n'
              ' - Выбрать другие товары представленные выше\n'
        ),
        reply_markup=under_want_buy_keyboard(item_id)
    )
    await call.message.delete()


@shop_router.callback_query(F.data.contains('change_count:'))
async def change_count(call: CallbackQuery):
    _, item_id = call.data.split(': ')
    await call.message.answer(
        text='Выберите необходимое количество',
        reply_markup=two_to_five_keyboard(item_id)
    )


@shop_router.callback_query(F.data.contains('this_count:'))
async def this_count(call: CallbackQuery, state: FSMContext):
    _, num, item_id = call.data.split(': ')
    data = await state.get_data()
    full_cart = data.get('cart')
    item_list = full_cart.get(item_id)
    item_list.pop()
    item_list.append(num)
    full_cart[item_id] = item_list
    await state.update_data(cart=full_cart)
    await call.message.answer(
        text=(f'Товар: {item_list[0]} - стоимостью: {item_list[1]} рублей - в количестве: {item_list[2]}\n'
              '\nДобавлен в корзину\n'
              '\n'
              'Вы можете:\n'
              '\n'
              ' - Cформировать корзину\n'
              ' - Изменить количество товара\n'
              ' - Выбрать другие товары представленные выше\n'
        ),
        reply_markup=under_want_buy_keyboard(item_id)
    )
    await call.message.delete()


@shop_router.callback_query(F.data.contains('other_count:'))
async def other_count(call: CallbackQuery, state: FSMContext):
    _, item_id = call.data.split(': ')
    await call.message.answer('Введите необходимое количество:')
    await call.message.delete()
    await state.update_data(id_item=item_id)
    await state.set_state(Item.id_item)


@shop_router.message(F.text.regexp(r'^(\d+)$').as_('digits'), Item.id_item)
async def other_count_get(message: Message, state: FSMContext):
    num = int(re.sub(r'[^0-9]', '', message.text))
    data = await state.get_data()
    item_id = data.get('id_item')
    full_cart = data.get('cart')
    item_list = full_cart.get(item_id)
    item_list.pop()
    item_list.append(num)
    full_cart[item_id] = item_list
    await state.update_data(cart=full_cart)
    await state.update_data(item_id=None)
    await message.answer(
        text=(f'Товар: {item_list[0]} - стоимостью: {item_list[1]} рублей - в количестве: {item_list[2]}\n'
              '\nДобавлен в корзину\n'
              '\n'
              'Вы можете:\n'
              '\n'
              ' - Cформировать корзину\n'
              ' - Изменить количество товара\n'
              ' - Выбрать другие товары представленные выше\n'
        ),
        reply_markup=under_want_buy_keyboard(item_id)
    )


@shop_router.callback_query(F.data.contains('show_cart'))
async def show_cart(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart: dict = data.get('cart')
    text = 'Корзина 🛒: \n\n'
    amount = 0
    for item_id, list_values_item in cart.items():
        text += (
            f'Товар: {list_values_item[0]} - стоимость: {list_values_item[1]} рублей - количество: {list_values_item[2]}'
            '\n'
        )
        amount += int(list_values_item[1]) * int(list_values_item[2])
    text += (
        '\n'
        f'Итоговая стоимость: {amount}'
    )
    await call.message.answer(
        text=text,
        reply_markup=choose_logistic_keyboard()
    )
    await state.update_data(cart_for_dasha=text)


@shop_router.callback_query(F.data == 'choose_logistic')
async def choose_logistic(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.answer(
        text=(
            'Для доставки понадобятся Ваши контактные данные\n'
            'Введите, пожалуйста, Ваши ФИО:'
        ),
    )
    await state.set_state(Item.fio)


@shop_router.message(F.text, Item.fio)
async def get_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Item.adress)
    await message.answer(
        text='ФИО записали!\nТеперь нужен адрес или индекс:'
    )


@shop_router.message(F.text, Item.adress)
async def get_adress(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    await state.set_state(Item.phone)
    await message.answer(
        text=('Адрес записан!\n'
        'Остался телефон, можно поделится контактом или ввести вручную:'),
        reply_markup=share_contact_keyboard()
    )


@shop_router.message(Item.phone)
async def get_phone(message: Message, state: FSMContext):
    if not message.contact:
        await state.update_data(phone=message.text)
    else:
        await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Item.logistic)
    await message.answer(
        text='Напишите предпочтительную логистическую фирму (Кроме СДЕК, с ними не работаем):',
        reply_markup=logistic_keyboard()
    )


@shop_router.message(Item.logistic)
async def get_logistic(message: Message, state: FSMContext):
    await state.update_data(logistic=message.text)
    await message.answer(
        text='Теперь самое интересное, перейдем к оплате?',
        reply_markup=pay_order_keyboard()
    )


@shop_router.callback_query(F.data == 'pay_order')
async def pay_order(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.answer(
        text=(
            'Благодарю Вас за заказ!\n'
            'Даша свяжется с Вами в ближайщее время для подтверждения!\n\n'
            'А пока Вы можете оправить деньги через приложение любого банка: \n'
            'Тинькофф - по номеру телефона +79500638409 (получатель Дарья Никитична Г)\n'
            'или используя реквизиты ниже 👇'
        ),
    )
    await bot.send_photo(
        call.message.chat.id,
        photo='https://i.yapx.ru/YZ9SK.jpg',
        caption='Это реквизиты для удобного перевода через Т-Банк :)'
        )
    data = await state.get_data()
    cart = data.get('cart_for_dasha')
    fio = data.get('fio')
    adress = data.get('adress')
    phone = data.get('phone')
    logistic = data.get('logistic')
    
    await bot.send_message(
        -4658422924,
        text=(
            f'Клиент @{call.from_user.username}\n'
            f'{cart}\n\n'
            f'Контактная информация: \n\n'
            f'ФИО: {fio}\nАдрес: {adress}\nТелефон: {phone}\n'
            f'Предпочтительная логистическая фирма: {logistic}\n'
        )
    )
    
    await state.clear()
