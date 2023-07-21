import os
import re

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    edit_text = re.sub(r'[.,!?:;]\.+$', '', text[start:start+size])
    edit_text = re.findall(r'(?s).+[.,!?:;]', edit_text)
    edit_text = edit_text.lstrip()  # убирает лишние \n
    return edit_text, len(edit_text)


def prepare_book(path: str) -> None:
    page_num = 1
    start = 0
    with open(path, 'r') as my_book:
        text = my_book.read()
        while True:
            if len(text) > PAGE_SIZE:
                text = text[start:]
            else:
                break
            res = _get_part_text(text, 0, PAGE_SIZE)
            book[page_num] = res[0].lstrip()
            start = res[1]
            page_num += 1


prepare_book(os.path.join(os.getcwd(), BOOK_PATH))