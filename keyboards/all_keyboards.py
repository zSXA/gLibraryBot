from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from create_bot import admins
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📚 Книги!")],
        [KeyboardButton(text="❓ Помощь")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True, 
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
        )
    return keyboard

def create_list_books(data: list, message: Message):
    user = f'{message.from_user.first_name}, @{message.from_user.username}'
    books = []
    for item in data:
        book = item['Название книги'].strip()
        if item['Читатель'] != '':
            if item['Читатель'] == user:
                book = '📖' + book
            else:
                book = '📍' + book
        books.append(book)

    builder = ReplyKeyboardBuilder()
    for book in books:
        builder.button(text=book)
    builder.button(text='Назад')
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)