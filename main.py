import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.shop_handlers import shop_router
from handlers.about_me import about_me_router
# from time_func.send_message import create_schedule
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot):
    commands = [BotCommand(command='/start', description='Начало'),]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands(bot)


async def main():
    dp.include_router(start_router)
    dp.include_router(shop_router)
    dp.include_router(about_me_router)
    dp.startup.register(start_bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
