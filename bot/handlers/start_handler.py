import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

logger = logging.getLogger(__name__)

start_router = Router()

@start_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("🔍 Demon Cry OSINT Agent.\nОтправь мне цель для расследования.")
