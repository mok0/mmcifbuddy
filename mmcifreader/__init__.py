import sys
from loguru import logger
from mmcifreader.timer import Timer
from mmcifreader import mmciflexer as lex


logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm}</green> <level>{message}</level>")


def parse(fname, verbose=False) -> dict:
 
    status = lex.open_file(fname)

    # If we didn't get non zero status, bail out, otherwise
    # get_token() is stuck.
    if not status:
        logger.error(f"Input file not found ({fname})")
        raise SystemExit

    typ, token = lex.get_token()

    D = {}
    wait = False
    while typ:
        match typ:
            case lex.tID:
                if verbose:
                    logger.info(f"tID {token}")

            case lex.tDATA:
                #print("tDATA",typ, token)
                pass

            case lex.tNAME:
                name = token
                typ, token = lex.get_token()
                if typ != lex.tDATA:
                    if typ == lex.tDATALINE_BEGIN:
                        handle_dataline(D, name, token)
                    else: # We always expect data after a name
                        typ_nam = lex.return_type_names[typ]
                        logger.error(f"Something went wrong with {name}, typ = {typ_nam}, token = {token}")
                        print(D)
                        raise SystemError
                    #.    
                    D[name] = token

            case lex.tLOOP:
                typ, token = handle_loop(D)
                wait = True

            case lex.tCOMMENT:
                pass
 
            case _:
                logger.warning(f"What is this? typ = {typ}, token = {token}")

        if not wait: # handle_loop already has next typ, token
            typ, token = lex.get_token()
        wait = False

    lex.close_file()
    return D
 

def handle_loop(D) -> tuple[str, str]:

    Q = []
    loopdata = []
    typ, token = lex.get_token()
    while typ == lex.tNAME:
        Q.append(token)
        typ, token = lex.get_token()
    qsize = len(Q)
 
    # Create empty datastructure to store the loop data
    for _ in range(qsize):
        loopdata.append([])

    col = 0
    while typ == lex.tDATA:
        loopdata[col].append(token)
        col += 1
        if col > qsize-1:
            col = 0
        typ, token = lex.get_token()
        if typ != lex.tDATA:
            break
 
    for i, name in enumerate(Q):
        D[name] = loopdata[i]

    # return next token that we are not using
    return typ, token
 

def handle_dataline(D, name, firsttoken) -> None:
    L = [firsttoken]

    typ, token = lex.get_token()
    while typ != lex.tDATALINE_END:
        L.append(token)
        typ, token = lex.get_token()

    # We still need the last token
    #L.append(token) # no it's just ;\n
    D[name] = L
