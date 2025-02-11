import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from typing import Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from google_handler.GoogleTable import GoogleTable
import os

#from db_handler.db_class import PostgresHandler

#pg_db = PostgresHandler(config('PG_LINK'))
scheduler = AsyncIOScheduler(timezone='Asia/Yekaterinburg')
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')

sheet_title = config('sheet_title_books')
google_table = GoogleTable(config('google_config_auth'),config('google_table_key'))
google_table.get_data_from_sheet(sheet_title, 7)
books = [item['Название книги'].strip() for item in google_table.data]
batch_data: Dict = {}