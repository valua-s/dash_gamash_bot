from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from google_sheets_records.record_to_google_sheets import RecordProka44ai
from decouple import config


def start_keyboard():
    
    inline_kb_list = [
        [InlineKeyboardButton(
            text='Весь ассортимент магазина 🛍️', callback_data='shop_assortiment'
            )],
        [InlineKeyboardButton(
            text='Обо мне 👨‍💻', callback_data='about_me'
        )],]
    
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def accept_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(
            text='Да, все верно', callback_data='accept_record'
            )],
        [InlineKeyboardButton(
            text='Нет, хочу вернуться и выбрать другое...', callback_data='change_record'
            )],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def cancel_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(
            text='Да, все верно', callback_data='delete_record'
            )],
        [InlineKeyboardButton(
            text='Нет, хочу вернуться и выбрать другое...', callback_data='change_record'
            )],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def payment_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(
            text='Отправил по номеру телефона', callback_data='by_number_payment',
            )],
        [InlineKeyboardButton(
            text='Оплачу наличными при встрече', callback_data='by_cash_payment'
            )],
        # [InlineKeyboardButton(
        #     text='Оплата онлайн', callback_data='online_payment'
        #     )],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
