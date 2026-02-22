from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from finance_bot.keyboards.main import main_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Выбирай:", reply_markup=main_kb)
