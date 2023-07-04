from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message
from random import randint
from environs import Env

env = Env()
env.read_env()
bot_token = env('API_TOKEN')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher()

users = {}


def check_user(u_id):
    """Checks if user ever launched the bot"""
    if u_id not in users:
        users[u_id] = {'in_game': False,
                       'secret_number': None,
                       'ATTEMPTS': None,
                       'total_games': 0,
                       'wins': 0,
                       'attempts_global': 5,
                       'start_dig': 1,
                       'end_dig': 100}


# хэндлер команды "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nСыграем в числовую угодайку?')
    check_user(message.from_user.id)


# хэндлер команды "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    user_id = message.from_user.id
    check_user(user_id)
    await message.answer('Я угодайка от Алексея. Зогадываю число. Ты угодывуеш. '
                         'На етом все. Какой такой хелб\n'
                         'А впрочем\n\nКоманды такие:\n/cancel - выйти из игры\n'
                         '/stat - глянуть, кто из нас сильнее\n\n'
                         f'Сейчас Вам нужно угадать число от {users[user_id]["start_dig"]}'
                         f' до {users[user_id]["end_dig"]} за {users[user_id]["attempts_global"]} попыток\n'
                         'Чтобы поменять эти значения, наберите:\n'
                         'start_dig <число> - задать начало диапазона\n'
                         'end_dig <число> - задать конец диапазона\n'
                         'attempts <число> - задать количество попыток')


# хэндлер команды "/stat"
@dp.message(Command(commands=["stat"]))
async def process_start_command(message: Message):
    user_id = message.from_user.id
    check_user(user_id)
    await message.answer(f'Количество игр - {users[user_id]["total_games"]}\n'
                         f'Выиграно из них - {users[user_id]["wins"]}')


# хэндлер команды "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    user_id = message.from_user.id
    check_user(user_id)
    if users[user_id]['in_game']:
        await message.answer('Игра окончена, вы проиграли, штош')
        users[user_id]["total_games"] += 1
        users[user_id]['in_game'] = False
    else:
        await message.answer('Ну, ну, мы же еще и не начинали!\n'
                             'Кстати, как насчет?')


# хэндлер согласия
@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def process_positive_answer(message: Message):
    user_id = message.from_user.id
    check_user(user_id)
    if not users[user_id]['in_game']:
        await message.answer(f'Такс такс такс, что тут у нас?\n'
                             f'Угодайка угодайка ахах наканецта\n'
                             f'\nЯ загадал число от {users[user_id]["start_dig"]} до {users[user_id]["end_dig"]},\n'
                             f'попробуй угадать! Осталось {users[user_id]["attempts_global"]} попыток')
        users[user_id]['in_game'] = True
        users[user_id]['secret_number'] = randint(users[user_id]['start_dig'], users[user_id]['end_dig'])
        users[user_id]['ATTEMPTS'] = users[user_id]['attempts_global']
    else:
        await message.answer('Пока мы играем, я могу '
                             f'реагировать только на числа от {users[user_id]["start_dig"]} до {users[user_id]["end_dig"]} '
                             'и команды /cancel и /stat')


# хэндлер отказа
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    user_id = message.from_user.id
    check_user(user_id)
    if not users[user_id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             f'пожалуйста, числа от {users[user_id]["start_dig"]} '
                             f'до {users[user_id]["end_dig"]}')


# хэндлер игры
@dp.message(lambda x: x.text and x.text.isdigit())
async def process_numbers_answer(message: Message):
    user_id = message.from_user.id
    check_user(user_id)
    if users[message.from_user.id]["start_dig"] <= int(message.text) <= users[message.from_user.id]["end_dig"]:
        if users[user_id]['in_game']:
            if int(message.text) == users[user_id]['secret_number']:
                await message.answer('О ну и ну! В смысле, да, Вы угодали!\n\n'
                                     'Еще партейку?')
                users[user_id]['in_game'] = False
                users[user_id]['total_games'] += 1
                users[user_id]['wins'] += 1
            elif int(message.text) > users[user_id]['secret_number']:
                await message.answer('Мое число меньше')
                users[user_id]['ATTEMPTS'] -= 1
            elif int(message.text) < users[user_id]['secret_number']:
                await message.answer('Мое число больше')
                users[user_id]['ATTEMPTS'] -= 1

            if users[user_id]['ATTEMPTS'] == 0:
                await message.answer(f'К сожалению, у вас больше не осталось '
                                     f'попыток. Вы проиграли :(\n\nМое число '
                                     f'было {users[user_id]["secret_number"]}\n\nДавайте '
                                     f'сыграем еще?')
                users[user_id]['in_game'] = False
                users[user_id]['total_games'] += 1
        else:
            await message.answer('Мы еще не играем. Хотите сыграть?')
    else:
        if users[user_id]['in_game']:
            await message.answer('Нет такого числа в диапазоне вообще!\n'
                                 'Прощу Вашу невнимательность, не отниму попытку.')
        else:
            await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    user_id = message.from_user.id
    check_user(user_id)
    if users[user_id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             f'Присылайте, пожалуйста, числа от {users[user_id]["start_dig"]}'
                             f' до {users[user_id]["end_dig"]}')
    else:
        answer = message.text.split()
        if len(answer) == 2:
            if answer[0] == 'start_dig' and answer[1].isdigit():
                users[user_id]['start_dig'] = int(answer[-1])
                await message.answer('Хорошо')
            elif answer[0] == 'end_dig' and answer[1].isdigit():
                users[user_id]['end_dig'] = int(answer[-1])
                await message.answer('Не вопрос')
            elif answer[0] == 'attempts' and answer[1].isdigit():
                users[user_id]['attempts_global'] = int(answer[-1])
                await message.answer('Да пожалуйста')
            else:
                await message.answer('Нет нет неееет, что-то здесь не так')
        else:
            await message.answer('Етого я не понимаю, щто такое\n'
                                 'Давайте просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)
