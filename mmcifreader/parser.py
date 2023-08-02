import sys

import queue
from loguru import logger

from states import StateName, State, BeginState, LoopState


import mmcifreader as mr
from mmcifreader import mmciflexer as lex 



logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm}</green> <level>{message}</level>")



def handle_dataline(parser) -> list:
    data = []

    while True: 
        # print("handle_dataline(), about to call parser.get_token()")
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
        category, item = token.split('.')
        Q.append((category, item))
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
        #print("handle_loop()2 , about to call parser.get_token()")
        typ, token = parser.get_token()
        if typ == lex.tDATALINE_BEGIN:
            #thelist = handle_dataline(parser) 
            thelist = []
            loopdata[col].append(thelist)
    
    for i, tok in enumerate(Q):
        category, item = tok 
        if not D.get(category):
            D[category] = {}
        D[category][item] = loopdata[i]

    #logger.warning(f"In handle_loop, typ = {lex.token_type_names[typ]}, token = {token}")
    parser.unget.put((typ, token))
    return D
 

class Parser:  
    """Context class 'state of states' """
    def __init__(self, fname) -> None:
 
        self.begin_state = BeginState(self)
        ###self.end_of_file_state = EndOfFileState(self)
        ###self.id_state = IdState(self)
        self.loop_state = LoopState(self)
     
        self.state = self.begin_state
        self.statename = StateName.sBEGIN
        self.fname = fname
        self.typ = None
        self.token = None
        self.queue = queue.SimpleQueue()
        self.unget = queue.SimpleQueue()
        self.data_blocks = {}
        self.current_dict = None
        self.current_category = None
        self.current_category_dict = None


    def set_state(self, statename: StateName, state: State) -> None:
        self.state = state
        self.statename = statename
 

    def open(self):
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
        

    def close(self):
        # Call lexer to close file
        lex.close_file()


    def get_token(self):

        if self.unget.empty():
            self.typ, self.token = lex.get_token()
        else:
            self.typ, self.token = self.unget.get()

        #logger.debug(f"get_token, state is now {self.state}, typ is {lex.token_type_names[self.typ]}")
        return self.typ, self.token


    def parse(self):
        # Main loop
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
                        category, item = token.split('.')
                        if category not in self.current_dict:
                            self.current_dict[category] = {}
                        self.queue.put((category, item))                     

                case lex.tDATA:
                    if self.statename != StateName.sLOOP:
                        category, item = self.queue.get()
                        if category not in self.current_dict:
                            self.current_dict[category] = {}
                        self.current_dict[category][item] = token
                    else:
                        handle_dataline(parser)

                case lex.tDATALINE_BEGIN:
                    data = handle_dataline(parser)

                    if self.statename != StateName.sLOOP:
                        category, item = self.queue.get()
                        self.current_dict[category][item] = data

                case lex.tLOOP:
                    self.set_state(StateName.sLOOP, self.loop_state) 
                    D = handle_loop(parser)
                    self.current_dict.update(D)
                   
                case lex.tLOOP_END:                               
                    self.set_state(StateName.sBEGIN, self.begin_state)
                  
                case lex.tCOMMENT:
                    pass

                case lex.tEND_OF_FILE:
                    #self.set_state(StateName.sEND_OF_FILE, self.end_of_file_state)
                    self.close()
                    break

                case _:
                    logger.warning(f"Not handling {lex.token_type_names[typ]}, state: {parser.statename} ")                         

        logger.info("Done parsing")










if __name__ == "__main__":
    import pprint
    from pathlib import Path
    from mmcifreader.timer import Timer

    pp = pprint.PrettyPrinter(indent=2)
    clock = Timer()
    clock.start()
    path = Path('data', '4af1.cif')
    parser = Parser(path)
    parser.open()
    parser.parse()
    clock.stop()

    #pp.pprint(parser.data_blocks)
    print(parser.data_blocks.keys())
    print(parser.current_dict.keys())
    pp.pprint(parser.current_dict['_atom_sites'])

 