import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.config import config

from bot.handlers import (
    start_handler,
    investigate_handler,
)


logger = logging.getLogger(__name__)

dp = Dispatcher()

bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN,
            link_preview_is_disabled=True
        )
)

dp.include_routers(
    start_handler.start_router,
    investigate_handler.investigate_router,
)


async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="старт | перезапуск бота"),
    ]
    await bot.set_my_commands(commands)


async def main():
    await set_bot_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info(f"Процесс прерван пользователем")