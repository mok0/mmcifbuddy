#     Copyright (C) 2023 Morten Kjeldgaard
import sys
import queue
from pathlib import Path
from loguru import logger
from .states import StateName, State, BeginState, LoopState
from mmcifreader import mmciflexer as lex

logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm}</green> <level>{message}</level>")


def handle_dataline(parser) -> list:
    # Handle the datalines
    data = []
    while True:
        typ, token = parser.get_token()
        if typ in (lex.tDATALINE_END, lex.tEND_OF_FILE):
            break
        data.append(token)
    return data


def handle_loop(parser) -> dict:
    # Handle the table data inside a loop. First comes a list of
    # column names, that determines the number of columns in the data.
    D = {}
    Q = []
    loopdata = []
    typ, token = parser.get_token()

    while typ == lex.tNAME:
        Q.append(token)
        typ, token = parser.get_token()
    qsize = len(Q)

    # We have all column names in loop_ structure
    # Create empty datastructure to store the loop data
    for _ in range(qsize):
        loopdata.append([])

    col = 0
    while typ in (lex.tDATA, lex.tDATALINE_BEGIN):
        loopdata[col].append(token)
        col += 1
        if col > qsize-1:
            col = 0
        typ, token = parser.get_token()
        if typ == lex.tDATALINE_BEGIN:
            thelist = handle_dataline(parser)
            loopdata[col].append(thelist)
        #.
    #.
    for i, name in enumerate(Q):
        D[name] = loopdata[i]

    parser.unget.put((typ, token))
    return D


class Parser:
    def __init__(self) -> None:

        self.begin_state = BeginState(self)
        self.loop_state = LoopState(self)
        self.state = self.begin_state
        self.statename = StateName.sBEGIN
        self.fname = None
        self.opened = False
        self.typ = None
        self.token = None
        self.queue = queue.SimpleQueue()
        self.unget = queue.SimpleQueue()
        self.data_blocks = {}
        self.current_dict = None
        self.simple = True


    def set_state(self, statename: StateName, state: State) -> None:
        self.state = state
        self.statename = statename

    def open(self, fname) -> None:
        self.fname = fname

        # Check if file exists and can be opened without errors,
        # then call lexer to open file.
        if isinstance(self.fname, Path):
            self.fname = str(self.fname)

        if not Path(self.fname).exists():
            logger.error("File not found")
            raise FileNotFoundError

        status = lex.open_file(self.fname)
        if not status:
            logger.error(f"Error opening file ({self.fname})")
            raise SystemExit
        self.opened = True


    def close(self) -> None:
        # Call lexer to close file
        lex.close_file()
        self.opened = False


    def get_token(self) -> tuple[str,str]:
        # Get next token from lexer
        if self.unget.empty():
            self.typ, self.token = lex.get_token()
        else:
            self.typ, self.token = self.unget.get()
        return self.typ, self.token


    def get_datablock_names(self) -> list:
        return list(self.data_blocks.keys())


    def parse(self) -> dict:

        if not self.opened:
            logger.error("Input file not open for reading")
            raise SystemExit

        typ = 1
        while typ:

            typ, token = self.get_token()

            match typ:
                case lex.tID:
                    if token not in self.data_blocks:
                        self.data_blocks[token] = {}
                    self.current_dict = self.data_blocks[token]

                case lex.tNAME:
                    if self.statename != StateName.sLOOP:
                        self.queue.put(token)

                case lex.tDATA:
                    if self.statename != StateName.sLOOP:
                        name = self.queue.get()
                        self.current_dict[name] = token

                case lex.tDATALINE_BEGIN:
                    data = handle_dataline(self)

                    if self.statename != StateName.sLOOP:
                        name = self.queue.get()
                        self.current_dict[name] = data

                case lex.tLOOP:
                    self.set_state(StateName.sLOOP, self.loop_state)
                    D = handle_loop(self)
                    self.current_dict.update(D)

                case lex.tLOOP_END:
                    self.set_state(StateName.sBEGIN, self.begin_state)

                case lex.tCOMMENT:
                    pass

                case lex.tEND_OF_FILE:
                    self.close()
                    break

                case _:
                    logger.warning(f"Not handling {lex.token_type_names[typ]}, state: {self.statename} ")

        logger.info(f"Done parsing {self.get_datablock_names()}")
        return self.data_blocks
