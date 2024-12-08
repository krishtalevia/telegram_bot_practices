import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject

import datetime

token = '7581111496:AAFXdQGFs6dORM0FbNyyLMp33HTman8q_X8'

bot = Bot(token = token)

dp = Dispatcher()

@dp.message(Command('start'))
async def start_handler(message: types.Message) -> None:
    await message.reply('Бот помогает пользователю составить план дня, добавляя задачи с указанием времени и пометками о приоритете.')

@dp.message(Command('add_task'))
async def add_task_handler(message: types.Message, command: CommandObject) -> None:
    if command.args is None:
        await message.answer(
            '/add task принимает два параметра: <время> <описание> ' +
            '— добавляет задачу (например, /add_task 12:00 Купить продукты).'
            )
        return
    
    if len(command.args.split()) != 2:
        await message.answer(
            '/add task принимает два параметра: <время> <описание> ' +
            '— добавляет задачу (например, /add_task 12:00 Купить продукты).'
            )
        return
    
    time = str(command.args[0:5])
    task = str(command.args[6::])

    try:
        time = time.strptime(time, '%H:%M')
    except ValueError:
        await message.answer('Команда должна содержать в себе время в формате чч:мм.')

async def main():
    await dp.start_polling(bot)

if __name__ = '__main__':
    asyncio.run(main())