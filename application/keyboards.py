from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Каталог", callback_data="catalog")
    builder.button(text="Отправить заявку", callback_data="request")
    builder.adjust(2)
    return builder.as_markup()


def jobs():
    jobs_builder = InlineKeyboardBuilder()
    jobs_builder.button(text="Frontend", callback_data="frontend")
    jobs_builder.button(text="Backend", callback_data="backend")
    jobs_builder.adjust(2)
    return jobs_builder.as_markup()
