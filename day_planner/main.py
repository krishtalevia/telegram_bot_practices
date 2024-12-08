import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from config import TOKEN
import time

bot = Bot(token = TOKEN)
dp = Dispatcher()

user_tasks = {}

def add_user_task(user_id: int) -> None:
    if user_id not in user_tasks.keys():
        user_tasks[user_id] = {}

@dp.message(Command('start'))
async def start_handler(message: types.Message) -> None:
    await message.reply('Бот помогает пользователю составить план дня, добавляя задачи с указанием времени и пометками о приоритете.')

@dp.message(Command('add_task'))
async def add_task_handler(message: types.Message, command: CommandObject) -> None:
    add_user_task(message.chat.id)

    command_description = '/add task принимает два параметра: <время> <описание> — добавляет задачу (например, /add_task 12:00 Купить продукты).'

    if command.args is None:
        await message.answer(command_description)
        return
    
    args = command.args.split()
    if len(args) < 2:
        await message.answer(command_description)
        return
    
    time_str = args[0]
    task = ' '.join(args[1:])

    try:
        time.strptime(time_str, '%H:%M')
    except ValueError:
        await message.answer('Команда должна содержать в себе время в формате чч:мм.')
        return

    user_tasks[message.chat.id][time_str] = task
    await message.answer(f'Задача "{task}" добавлена на {time_str}')

@dp.message(Command('show_tasks'))
async def show_tasks_handler(message: types.Message) -> None:
    add_user_task(message.chat.id)

    tasks = user_tasks[message.chat.id]
    if len(tasks) == 0:
        await message.reply(f'У вас нет задач.')
        return
    
    tasks_list = []
    for time, task in tasks.items():
        tasks_list.append(f'{time}: {task}')

    await message.answer('\n'.join(tasks_list))

@dp.message(Command('remove_task'))
async def remove_task_handler(message: types.Message, command: CommandObject) -> None:
    add_user_task(message.chat.id)

    if command.args is None:
        await message.reply('Укажите время задачи, для ее удаления (чч:мм)')
        return
    
    chosen_time = command.args
    if chosen_time in user_tasks[message.chat.id]:
        del user_tasks[message.chat.id][chosen_time]
        await message.answer('Задача на {chosen_time} удалена.')
    else:
        await message.answer('Задачи на {chosen_time} не найдено.')

@dp.message(Command('clear_tasks'))
async def clear_tasks_handler(message: types.Message) -> None:
    add_user_task(message.chat.id)
    user_tasks[message.chat.id].clear()
    await message.answer('Все задачи удалены.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())