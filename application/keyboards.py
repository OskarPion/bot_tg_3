from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Каталог", callback_data="catalog")
    builder.adjust(1)
    return builder.as_markup()
