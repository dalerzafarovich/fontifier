import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from aiopg.sa import create_engine
from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware

from tgbot.handlers.fontify import register_fontify
from tgbot.handlers.info import register_info
from tgbot.handlers.inline_mode import register_inline

logger = logging.getLogger(__name__)


async def create_pool(user, password, database, host, echo, port):
    print(host)
    return await create_engine(user=user, password=password, database=database, host=host, echo=echo, port=port)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage(host=config.redis.host, port=config.redis.port, password=config.redis.password)
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)

    if config.tg_bot.use_db:
        pool = await create_pool(
            user=config.db.user,
            password=config.db.password,
            database=config.db.database,
            host=config.db.host,
            echo=False,
            port=config.db.port
        )
        register_user(dp)
        dp.middleware.setup(DbMiddleware(pool))

    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)

    register_fontify(dp)
    register_info(dp)
    register_inline(dp)
    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        cmds = [['C:/Windows/system32/HOSTNAME.EXE']]
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
