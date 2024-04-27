import config
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!')


@router.message(Command('buy'))
async def cmd_buy(message: Message):
    await message.answer('Введите номер товара сообщением ниже.', reply_markup=create_keyboard())


class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: int


def create_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Купить",
        callback_data=MyCallback(foo="buy", bar="42")
    )
    return builder.as_markup()


@router.callback_query(MyCallback.filter(F.foo == "buy"))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    await query.message.answer('КНОПКА НАЖАТА')

    print("bar =", callback_data.bar)


async def main():
    bot = Bot(config.TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен.')
