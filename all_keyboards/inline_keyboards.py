from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from decouple import config


def start_keyboard():
    
    inline_kb_list = [
        [InlineKeyboardButton(
            text='Весь ассортимент магазина 🛍️', callback_data='shop_assortiment page: 1'
            )],
        [InlineKeyboardButton(
            text='Обо мне 👨‍💻', callback_data='about_me'
        )],]
    
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def under_item_keyboard(item_id, message_id, show_cart=None):

    inline_kb_list = [
        [InlineKeyboardButton(
            text='Добавить в корзину 🛍️', callback_data=f'item_id: {item_id}: {message_id}'
            )],
        ]

    if show_cart:
        inline_kb_list.insert(
            1,
            [InlineKeyboardButton(
                text='Показать корзину 🛒', callback_data='show_cart'
            )]
        )
    
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list, one_time_keyboard=True)


def show_next_page(next_page):
    inline_kb_list = [
        [
        InlineKeyboardButton(
            text='Следующая страница 🛍️', callback_data=f'shop_assortiment page: {next_page}'
        )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def under_want_buy_keyboard(item_id):
    inline_kb_list = [
        [
            InlineKeyboardButton(
                text='Показать корзину 🛒', callback_data='show_cart'
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить количество', callback_data=f'change_count: {item_id}'
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def two_to_five_keyboard(item_id):
    inline_kb_list = []
    for num in range(2, 6):
        inline_kb_list.append([InlineKeyboardButton(text=str(num), callback_data=f'this_count: {num}: {item_id}')])
    inline_kb_list.append([InlineKeyboardButton(text='Другое количество', callback_data=f'other_count: {item_id}')])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list, one_time_keyboard=True)


def choose_logistic_keyboard():
    inline_kb_list = [
        [
            InlineKeyboardButton(
                text='Перейти к выбору доставки 🚚', callback_data='choose_logistic'
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def share_contact_keyboard():
    kb_list = [
        [
            KeyboardButton(
                text='Поделится контактом 📱', request_contact=True
            )
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb_list, one_time_keyboard=True, resize_keyboard=True)


def logistic_keyboard():
    kb_list = [
        [
            KeyboardButton(
                text='Почта России 📮'
            )
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb_list, one_time_keyboard=True, resize_keyboard=True)


def pay_order_keyboard():
    inline_kb_list = [
        [
            InlineKeyboardButton(
                text='Оплатить заказ 💸', callback_data='pay_order'
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
