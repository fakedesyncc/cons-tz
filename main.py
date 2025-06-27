import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config
import openrouter_api

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработка команды /start"""
    await message.answer(
        "Бот для получения юридической информации по законодательству РФ.\n\n"
        "Просто напишите ваш вопрос, и я постараюсь помочь.\n\n"
        "Примеры запросов:\n"
        "- Федеральный закон о персональных данных\n"
        "- Статья 228 Уголовного кодекса\n"
        "- Как расторгнуть договор аренды?\n"
        "- Сроки уплаты НДФЛ\n\n"
        f"Используемые модели: {', '.join(config.OPENROUTER_MODELS)}"
    )


@dp.message(Command("models"))
async def cmd_models(message: types.Message):
    """Показать доступные модели"""
    models_list = "\n".join([f"- {model}" for model in config.OPENROUTER_MODELS])
    await message.answer(f"Доступные модели:\n{models_list}")


@dp.message()
async def handle_other_messages(message: types.Message):
    """Обработка всех сообщений как юридических запросов"""
    if message.text.startswith("/"):
        return

    try:
        await message.answer("Обработка вашего запроса...")
        response = openrouter_api.get_legal_response(message.text)
        await message.answer(response)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")


async def main():
    logger.info("Бот 'Поиск законов' запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
