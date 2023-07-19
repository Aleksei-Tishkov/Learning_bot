from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_RU, LEXICON

button_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
button_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])

yes_no_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

yes_no_kb_builder.row(button_yes, button_no, width=2)

yes_no_kb: ReplyKeyboardMarkup = yes_no_kb_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)

button_1: KeyboardButton = KeyboardButton(text=LEXICON_RU['rock'])
button_2: KeyboardButton = KeyboardButton(text=LEXICON_RU['scissors'])
button_3: KeyboardButton = KeyboardButton(text=LEXICON_RU['paper'])
button_4: KeyboardButton = KeyboardButton(text=LEXICON_RU['lizard'])
button_5: KeyboardButton = KeyboardButton(text=LEXICON_RU['spoc'])

BUTTONS: dict[str, str] = {'btn_1': '1',
                           'btn_2': '2',
                           'btn_3': '3',
                           'btn_4': '4',
                           'btn_5': '5'}

url_button_rules: InlineKeyboardButton = InlineKeyboardButton(
    text='Правила на вики', url='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C,_%D0%BD%D0%BE%D0%B6%D0%BD%D0%B8%D1%86%D1%8B,_%D0%B1%D1%83%D0%BC%D0%B0%D0%B3%D0%B0#%D0%91%D0%BE%D0%BB%D1%8C%D1%88%D0%B5_%D1%84%D0%B8%D0%B3%D1%83%D1%80'
)
url_button_video: InlineKeyboardButton = InlineKeyboardButton(text='Шелдон объясняет', url='https://youtu.be/_blQfsOvDps')

rules_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [url_button_rules], [url_button_video]
])

game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[
                                        [button_1],
                                        [button_2],
                                        [button_3],
                                        [button_4],
                                        [button_5]],
                                    resize_keyboard=True)

def create_inline_kb(width: int,
                     *args: str,
                     last_btn: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
                            text=last_btn,
                            callback_data='last_btn'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()