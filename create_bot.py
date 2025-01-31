import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler


admins = [int(admin_id) for admin_id in config('ADMINS').split(', ')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler(timezone='Asia/Yekaterinburg')
