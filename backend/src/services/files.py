import string
from config.log import Logger
from config.config import settings
from typing import Generator
from ..utils.utils import prepare_data, open_csvfile
from collections import Counter
import csv


log = Logger(__name__, 'log.log').logger


async def process_file(files: Generator):
    files = await create_csv_file(files)
    await add_files_to_db(files)
    return files


async def create_csv_file(files):
    async for filename, line in open_file(files):
        with open_csvfile(filename, mode='w') as csvfile:
            counter = Counter(line.split())
            writer = csv.DictWriter(
                csvfile, fieldnames=counter.keys(), quoting=csv.QUOTE_NONNUMERIC
            )
            writer.writeheader()
            writer.writerow(counter)


async def open_file(files: Generator):
    for file in files:
        try:
            byt = await file.read()
            yield file.filename, await prepare_data(byt)
        finally:
            await file.close()


async def add_files_to_db(files):
    pass

