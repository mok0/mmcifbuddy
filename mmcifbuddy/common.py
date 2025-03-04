from mmcifbuddy import mmciflexer as lex

def _handle_dataline(parser, token) -> list:
    # Handle the datalines
    data = [token]
    while True:
        typ, token = parser._get_token()
        if typ in (lex.tDATALINE_END, lex.tEND_OF_FILE):
            break
        data.append(token)
    return data
