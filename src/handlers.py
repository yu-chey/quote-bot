from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.config import hello_text
from src.db_manager import add_quote, select_all, delete_quote

from random import choice

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(hello_text)

@router.message(Command("add"))
async def add_handler(message: Message, command: CommandObject) -> None:
    quote_text = command.args

    if not quote_text or not quote_text.strip():
        await message.answer("❌ Вы не ввели текст цитаты. Используйте формат: /add [текст цитаты]")
        return

    await add_quote(quote_text.strip())

    await message.answer("✅ Ваша цитата добавлена!")

@router.message(Command("all"))
async def all_handler(message: Message) -> None:
    quotes = [f"{quote_id}: {quote_text}" for quote_id, quote_text in await select_all()]

    await message.answer("\n".join(quotes))

@router.message(Command("del"))
async def del_handler(message: Message) -> None:
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.answer("❌ Укажите ID цитаты. Пример: /del 5")
            return

        quote_id = int(args[1])

    except ValueError:
        await message.answer("❌ ID цитаты должен быть числом.")
        return

    if await delete_quote(quote_id):
        await message.answer(f"✅ Цитата с ID {quote_id} успешно удалена!")
    else:
        await message.answer(f"❌ Цитата с ID {quote_id} не найдена или не удалена.")

@router.message(Command("random"))
async def random_handler(message: Message) -> None:
    all_quotes = await select_all()

    if not all_quotes:
        await message.answer("В базе данных еще нет ни одной цитаты. Добавьте первую с помощью /add!")
        return

    quote_tuple = choice(all_quotes)
    quote = f"{quote_tuple[0]}: {quote_tuple[1]}"

    await message.answer(f"Вам выпало:\n\n{quote}")