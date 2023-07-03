from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

with open('API.txt', 'r') as file:
    API_TOKEN: str = file.read()

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        x = message.text.lower()
    except:
        x = 'включ'
    if 'выключ' not in x:
        await message.send_copy(chat_id=message.chat.id)
        await message.reply('Всё, мне надоело повторять')
    else:
        await message.reply('Давай, рискни')


if __name__ == '__main__':
    dp.run_polling(bot)