from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from keyboards.all_keyboards import main_kb, create_list_books
from create_bot import google_table, sheet_title
from datetime import datetime

start_router = Router()

data = []
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
    user = f'{message.from_user.first_name}, @{message.from_user.username}'
    data = google_table.get_data_from_sheet(sheet_title, 7)
    books.clear()
    for item in data:
        books.append(item['Название книги'])
    
    await message.answer(text='Выберите книгу!', reply_markup=create_list_books(data, user))

@start_router.message(F.text == 'Назад')
async def go_back_home(message: Message):
    await message.answer(text='Главное меню!', reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text[1:].in_(books))
async def read_message(message: Message):
    user = f'{message.from_user.first_name}, @{message.from_user.username}'
    data = google_table.get_data_from_sheet(sheet_title, 7)
    row = books.index(message.text[1:])
    book = None
    for item in data: 
        if item['Название книги'] == message.text[1:]:
            book = item
    text=f'Ничего'
    if book != None:
        if book['Читатель'].strip() == '':
            text=f'Вы выбрали: <b>{message.text}</b>'
            google_table.update_cell_from_sheet(sheet_title, row=row+8, col=5, value=user)
        elif book['Читатель'] == user:
            text=f'Книга: <b>{message.text}</b> возвращена!'
            google_table.update_cell_from_sheet(sheet_title, row=row+8, col=5, value='')
        else:
            text=f'Книга занята. \n \
                   Читатель: {book['Читатель']}\n \
                   Когда взял: {book['Когда взял']}\n \
                   Срок: {book['Срок']}'
    await message.reply(text=text, reply_markup=main_kb(message.from_user.id))
    