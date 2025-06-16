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


def photo_video_keyboard():
    photo_video_builder = InlineKeyboardBuilder()
    photo_video_builder.button(text="Отправить фото", callback_data='send_photo')
    photo_video_builder.button(text="Отправить видео", callback_data='send_video')
    photo_video_builder.button(text="Отправить файл", callback_data='send_file')
    photo_video_builder.adjust(2)
    return photo_video_builder.as_markup()
