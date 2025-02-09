#     Copyright (C) 2023-2025 Morten Kjeldgaard
# pylint: disable=logging-fstring-interpolation

from . import mmciflexer
from .logger import logger

## Class that wraps mmciflexer in a file-like object, that is also
## context aware

class FileReader:
    def __init__(self, file):
        self.file = file
        self.mode = 'r'
        self.closed = True

    def __enter__(self):
        logger.info(f'Opening the file {self.file}.')
        mmciflexer.fopen(self.file)
        self.closed = False
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        logger.info(f'Closing the file {self.file}.')
        if not self.closed:
            status = mmciflexer.fclose()
        return False

    def __next__(self):
        token = mmciflexer.get_token()
        if not token[0]:
            raise StopIteration
        return token

    def __iter__(self):
        return self

    def get_token(self):
        token = mmciflexer.get_token()
        if not token[0]:
            raise StopIteration
        return token

    def close(self):
        return mmciflexer.fclose()
