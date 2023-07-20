import mmciflexer

# Class that wraps mmciflexer in a file-like object,
# that is also context aware

class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.mode = 'r'
        self.closed = True
 
    def __enter__(self):
        #print(f'Opening the file {self.filename}.')
        self.__fd = mmciflexer.open_file(self.filename)
        print(self.__fd)
        self.closed = False
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        #print(f'Closing the file {self.filename}.')
        if not self.closed:
            mmciflexer.close_file()
        return False

    def __next__(self):
        token = mmciflexer.get_token()
        if not token[0]:
            raise StopIteration
        return token

    def __iter__(self):
        return self


if __name__ == "__main__":
    with FileReader('../4af1.cif') as f:
        for s in f:
            print(s)