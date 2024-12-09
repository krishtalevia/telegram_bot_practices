import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from config import TOKEN

bot = Bot(token = TOKEN)
dp = Dispatcher()