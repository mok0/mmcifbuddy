# Copyright (C) 2023-2025 Morten Kjeldgaard
# pylint: disable=too-many-instance-attributes, line-too-long,
# pylint: disable=protected-access, no-member
# pylint: disable=logging-fstring-interpolation

import queue
from pathlib import Path
from mmcifbuddy import mmciflexer as lex
from .logger import logger
from .states import StateName, State, BeginState, LoopState
from .common import _handle_dataline


def _handle_loop(parser) -> dict:
    """Internal function to handle the table data inside a loop_ """

    # In a loop_ structure, first comes a list of column names
    # that determines the number of columns in the data
    D = {}
    Q = []
    loopdata = []
    typ, token = parser._get_token()

    while typ == lex.tNAME:
        Q.append(token)
        typ, token = parser._get_token()
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
        typ, token = parser._get_token()
        if typ == lex.tDATALINE_BEGIN:
            thelist = _handle_dataline(parser, token)
            loopdata[col].append(thelist)
        #.
    #.
    for i, name in enumerate(Q):
        D[name] = loopdata[i]

    parser.unget.put((typ, token))
    return D


class Parser:
    """
    Parser class to handle the parsing of a file in mmCIF format.
    The class has the following public facing methods:

     - open(fp) -> None
       Method to pass an open Python file object to the parser, that
       has been opened with the Python open() statement, likely
       within a 'with' context. Otherwise the file must be closed by the
       caller and not by this class.

     - fopen(fname) -> None
       Method passing the name of the file to be processed. The
       file will be opened for reading in the module, and may
       be both plain and gzipped format.

     - fclose() -> None
       Method to close a file opened by fopen().

     - get_datablock_names() -> list
       This method returns a list of datablock names encountered during
       the parsing of the file.

     - reset() -> None:
       Reset the Parser class for reuse.

     - parse() -> dict
       This is the main parsing routine of the class, doing the actual
       work. It returns a dictionary of datablocks which again
       consists of dictionaries of categories. For a flat parser,
       use parser_flat instead.
    """

    def __init__(self, verbose=True) -> None:
        self.verbose = verbose
        self.begin_state = BeginState(self)
        self.loop_state = LoopState(self)
        self.state = self.begin_state
        self.statename = StateName.sBEGIN
        self.fname = None
        self.fp = None
        self.opened = False
        self.typ = None
        self.token = None
        self.queue = queue.SimpleQueue()
        self.unget = queue.SimpleQueue()
        self.data_blocks = {}
        self.current_dict = None
        self.flat = True

    def _reset(self) -> None:
        """Reset Parser class to initial state. Internal method that
        is called by fclose()."""
        self.fname = None
        self.fp = None
        self.opened = False
        self.typ = None
        self.token = None

    def _set_state(self, statename: StateName, state: State) -> None:
        """Set internal parser state"""
        self.state = state
        self.statename = statename

    def fopen(self, fname) -> None:
        """Open named file in C extension. File can be gzipped or not"""
        self.fname = fname

        # Check if file exists and can be opened without errors,
        # then call lexer to open file.
        if isinstance(self.fname, Path):
            self.fname = str(self.fname)

        if not Path(self.fname).exists():
            logger.error("File not found")
            raise FileNotFoundError

        status = lex.fopen(self.fname)
        if not status:
            logger.error(f"Error opening file ({self.fname})")
            raise SystemExit
        self.opened = True

    def open(self, fp) -> None:
        """Define file already opened in Python"""
        self.fp = fp

        if not hasattr(fp, 'fileno'):
            logger.error("Expecting open Python file object")
            raise TypeError()

        if fp.closed:
            logger.error("Expecting open file object")
            raise RuntimeError()

        status = lex.open(self.fp)
        if not status:
            logger.error(f"Error opening file ({self.fname})")
            raise SystemExit
        self.opened = True

    def fclose(self) -> None:
        """Call lexer to close file. Reset parser object"""
        if self.opened:
            lex.fclose()
        self._reset()

    def _set_debug_mode(self, value) -> int:
        """Set the internal debug mode in the lexer"""
        return lex.set_debug_mode(value)

    def _get_token(self) -> tuple[str, str]:
        """Internal method to get next token from lexer"""
        if self.unget.empty():
            self.typ, self.token = lex.get_token()
        else:
            self.typ, self.token = self.unget.get()
        return self.typ, self.token

    def get_datablock_names(self) -> list:
        """Return list of datablock names found in file"""
        return list(self.data_blocks.keys())

    def get_dict(self) -> dict:
        """Return the current (last) dictionary entry"""
        return self.current_dict

    def reset(self) -> None:
        """Reset class to initial state, this is relevant if the
        open() method of the parser is used, and the parser is needed
        to handle another file. The Parser class is reset
        automatically when the fopen() method is used in which case
        there is no need to call reset()
        """
        self._reset()

    def parse(self) -> dict:
        """
        Parse an mmCIF file. Returns a dict indexed by
        category.item keys.
        """

        if not self.opened:
            logger.error("Input file not open for reading")
            raise SystemExit

        typ = 1
        while typ:

            typ, token = self._get_token()

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
                    data = _handle_dataline(self, token)

                    if self.statename != StateName.sLOOP:
                        name = self.queue.get()
                        self.current_dict[name] = data

                case lex.tLOOP:
                    self._set_state(StateName.sLOOP, self.loop_state)
                    D = _handle_loop(self)
                    self.current_dict.update(D)

                case lex.tLOOP_END:
                    self._set_state(StateName.sBEGIN, self.begin_state)

                case lex.tCOMMENT:
                    pass

                case lex.tEND_OF_FILE:
                    break

                case lex.tSAVE_CATEGORY | lex.tSAVE_ITEM | lex.tSAVE_END:
                    logger.critical("Can't handle mmcif dictionaries")
                    raise SystemExit

                case _:
                    logger.warning(f"Not handling {lex.token_type_names[typ]}, state: {self.statename} ")

        if self.verbose:
            logger.info(f"Done parsing {self.get_datablock_names()}")
        return self.data_blocks
