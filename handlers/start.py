from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from keyboards.all_keyboards import main_kb, create_list_books
from create_bot import google_table, sheet_title

start_router = Router()

books = []

@start_router.message(CommandStart())
async def start(message: Message, command: CommandObject):
    command_args: str = command.args if command is not None else None
    hello_text = 'Привет!'
    await message.answer(text=hello_text, reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text == '❓ Помощь')
async def help(message: Message):
    await message.answer('Здесь будет инструкция:')

@start_router.message(F.text == '📚 Книги!')
async def get_books(message: Message):
    data = google_table.get_data_from_sheet(sheet_title, 7)
    for book in data:
        books.append(book['Название книги'].strip())
    await message.answer(text='Выберите книгу!', reply_markup=create_list_books(data, message))

@start_router.message(F.text == 'Назад')
async def go_back_home(message: Message):
    await message.answer(text='Главное меню!', reply_markup=main_kb(message.from_user.id))

@start_router.message()
async def read_message(message: Message):
    if message.text in books:
        row = books.index(message.text)
        user = f'{message.from_user.first_name}, @{message.from_user.username}'
        google_table.update_cell_from_sheet(sheet_title, row=row+8, col=5, value=user)
        await message.reply(text=f'Вы выбрали: <b>{message.text}</b>', reply_markup=main_kb(message.from_user.id))