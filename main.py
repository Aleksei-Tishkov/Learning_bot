from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message
from random import randint

with open('API.txt', 'r') as file:
    API_TOKEN: str = file.read()

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


user: dict = {'in_game': False,
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


# хэндлер команды "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Я угодайка от Алексея. Зогадываю число. Ты угодывуеш. '
                         'На етом все. Какой такой хелб\n'
                         'А впрочем\n\nКоманды такие:\n/cancel - выйти из игры\n'
                         '/stat - глянуть, кто из нас сильнее\n\n'
                         'По умолчанию Вам нужно угадать число от 1 до 100 за 5 попыток\n'
                         'Чтобы поменять эти значения, наберите:\n'
                         'start_dig <число> - задать начало диапазона\n'
                         'end_dig <число> - задать конец диапазона\n'
                         'attempts <число> - задать количество попыток')


# хэндлер команды "/stat"
@dp.message(Command(commands=["stat"]))
async def process_start_command(message: Message):
    await message.answer(f'Количество игр - {user["total_games"]}\n'
                         f'Выиграно из них - {user["wins"]}')


# хэндлер команды "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Игра окончена, вы проиграли, штош')
        user["total_games"] += 1
        user['in_game'] = False
    else:
        await message.answer('Ну, ну, мы же еще и не начинали!\n'
                             'Кстати, как насчет?')


# хэндлер согласия
@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        await message.answer(f'Такс такс такс, что тут у нас?\n'
                             f'Угодайка угодайка ахах наканецта\n'
                             f'\nЯ загадал число от {user["start_dig"]} до {user["end_dig"]},\n'
                             f'попробуй угадать! Осталось {user["attempts_global"]} попыток')
        user['in_game'] = True
        user['secret_number'] = randint(user['start_dig'], user['end_dig'])
        user['ATTEMPTS'] = user['attempts_global']
    else:
        await message.answer('Пока мы играем, я могу '
                             f'реагировать только на числа от {user["start_dig"]} до {user["end_dig"]} '
                             'и команды /cancel и /stat')

# хэндлер отказа
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             f'пожалуйста, числа от {user["start_dig"]} до {user["end_dig"]}')

# хэндлер игры
@dp.message(lambda x: x.text and x.text.isdigit() and user["start_dig"] <= int(x.text) <= user["end_dig"])
async def process_numbers_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            await message.answer('О ну и ну! В смысле, да, Вы угодали!\n\n'
                                 'Еще партейку?')
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
        elif int(message.text) > user['secret_number']:
            await message.answer('Мое число меньше')
            user['ATTEMPTS'] -= 1
        elif int(message.text) < user['secret_number']:
            await message.answer('Мое число больше')
            user['ATTEMPTS'] -= 1

        if user['ATTEMPTS'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое число '
                                 f'было {user["secret_number"]}\n\nДавайте '
                                 f'сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    if user['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             f'Присылайте, пожалуйста, числа от {user["start_dig"]} до {user["end_dig"]}')
    else:
        answer = message.text.split()
        if len(answer) == 2:
            if answer[0] == 'start_dig' and answer[1].isdigit():
                user['start_dig'] = int(answer[-1])
                await message.answer('Хорошо')
            elif answer[0] == 'end_dig' and answer[1].isdigit():
                user['end_dig'] = int(answer[-1])
                await message.answer('Не вопрос')
            elif answer[0] == 'attempts' and answer[1].isdigit():
                user['attempts_global'] = int(answer[-1])
                await message.answer('Да пожалуйста')
            else:
                await message.answer('Нет нет неееет, что-то здесь не так')
        else:
            await message.answer('Етого я не понимаю, щто такое\n'
                                 'Давайте просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)