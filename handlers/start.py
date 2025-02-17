import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from keyboards.keyboards import main_kb, create_list_books, admin_kb
from create_bot import google_table, books, admins, batch_data, scheduler, sheet_title, bot
from datetime import datetime
from filters.IsAdmin import IsAdmin
from typing import List
from utils.utils import gen_qrcode
from datetime import datetime, timedelta
start_router = Router()

data = google_table.data
weeks = iter(['2 недели', '3 недели', '4 недели', 'Ещё чуть-чуть'])


def rent(row: int, value: List):
    
    batch_data[f'E{row+8}:G{row+8}'] = value

    data[row]['Читатель'] = value[0]
    data[row]['Когда взял'] = value[1]
    data[row]['Срок'] = value[2]

def sync_table():
    if batch_data:
        google_table.update_range_from_sheet(sheet_title, batch_data)
    google_table.get_data_from_sheet(sheet_title, 7)

def refresh():
    if not scheduler.get_jobs():
        run_date = datetime.now() + timedelta(seconds=15.0)
        scheduler.add_job(func=sync_table, trigger='date', run_date=run_date,
                          id=f'sync_table_{run_date}', misfire_grace_time=5)
        
    for job in scheduler.get_jobs():
        print(f'ID job: {job.id}')
        print(f'Next run: {job.next_run_time}')
        print(f'State: {job._jobstore_alias}')

@start_router.message(CommandStart())
async def start(message: Message, command: CommandObject):

    if command.args:
        await read_message(message=message, command=command)

    hello_text = 'Привет! Выбери действие.'

    await message.answer(text=hello_text, reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text == '❓ Помощь')
async def help(message: Message):
    text = ('<b>❓ Помощь</b> - эта справка.\n'
            '<b>📚 Книги!</b> - список книг.\n'
            '📗 - книга доступна.\n'
            '📕 - книга занята.\n'
            '📘 - книга взята.'
    )
    await message.answer(text, reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text == '📚 Книги!')
async def get_books(message: Message):
    user = f'{message.from_user.first_name}, @{message.from_user.username}'
    await message.answer(text='Выберите книгу!', reply_markup=create_list_books(data, user))

@start_router.message(F.text == '⚙️ Админ панель', IsAdmin(admins))
async def get_books(message: Message):
    await message.answer(text='Воспользуйтесь меню.', reply_markup=admin_kb())

@start_router.message(F.text == 'Сгенерировать qr-code', IsAdmin(admins))
async def crcode(message: Message):
    await message.answer(text='Выберите книгу:', reply_markup=create_list_books(data))

@start_router.message(F.text.in_(books), IsAdmin(admins))
async def make_crcode(message: Message):
    book = message.text
    row=books.index(book)
    qrcode_path = gen_qrcode(book, f'https://t.me/USSC_lib_bot?start={row+1}')
    photo_file = FSInputFile(qrcode_path)
    await message.reply_photo(photo=photo_file, reply_markup=create_list_books(data), caption=f'Книга: <b>{book}</b>')

@start_router.message(F.text == 'Назад')
async def go_back_home(message: Message):
    await message.answer(text='Главное меню!', reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text[1:].in_(books))
async def read_message(message: Message, command = None):

    user = f'{message.from_user.first_name}, @{message.from_user.username}'

    book = None

    for item in data:
        if command:
            if item['ID'] == command.args:
                book = item
                break
        else:
            if item['Название книги'].strip() == message.text[1:]:
                book = item
                break
    
    await message.reply(text='Проверка картотеки 🤓 ...')

    text=f'Книга: {book} не найдена!'

    if book != None:
        row = data.index(book)
        book_name = book['Название книги'].strip()
        if book['Читатель'].strip() == '':
            i=0
            for item in data:
                if item['Читатель'] == user:
                    i+=1
            if i>1:
                text=f'Достигнут лимит книг. Верните книгу прежде чем взять новую.'
            else:
                text=f'Книга взята: <b>{book_name}</b>'
                rent(row=row, value=[user,
                                       datetime.now().strftime('%d.%m.%Y'),
                                       '2 недели'])
        elif book['Читатель'] == user:
            text=f'Книга возвращена: <b>{book_name}</b>'
            rent(row=row, value=['','',''])
        else:
            text=f'<b>Книга занята.</b>\n' + \
                 f'Читатель: {book['Читатель']}\n' + \
                 f'Когда взял: {book['Когда взял']}\n' + \
                 f'Срок: {book['Срок']}'
    print(batch_data)
    refresh()
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='typing'):
        await asyncio.sleep(2)
        await message.reply(text=text, reply_markup=create_list_books(data, user))