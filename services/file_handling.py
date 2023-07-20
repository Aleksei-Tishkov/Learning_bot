import os

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    pass

def prepare_book(path: str) -> None:
    pass

prepare_book(os.path.join(os.getcwd()), BOOK_PATH)