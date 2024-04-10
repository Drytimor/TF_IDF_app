from contextlib import AsyncExitStack, asynccontextmanager, contextmanager, ExitStack
from config.log import Logger
import string
import os
import re
from config.config import settings
import sys


log = Logger(__name__, 'log.log').logger


@contextmanager
def open_csvfile(
        filename: str, mode: str = 'r', **kwargs
):
    filename = create_path_to_csvfile(filename)

    file = open(filename, mode, newline='', **kwargs)

    try:
        yield file
    finally:
        file.close()


def create_path_to_csvfile(filename: str) -> str:
    file_csv = re.sub(r'\.txt', '.csv', filename)
    filepath = os.path.join(settings.DOWNLOAD_DIRECTORY, file_csv)
    return filepath


async def prepare_data(byt: bytes):
    s = byt.decode('utf-8').lower()
    table = str.maketrans('\n\t—', '   ', string.punctuation + string.digits)
    s = s.translate(table)
    return s


async def _TF_Function(word_frequency: int, total_number_words: int) -> float:
    return round(word_frequency / total_number_words, 4)


async def _IDF_Function(total_number_documents, number_documents_with_word) -> float:
    number_documents_with_word = number_documents_with_word if number_documents_with_word else 1
    return round(log10(total_number_documents / number_documents_with_word), 4)



