/* tEND_OF_FILE MUST be first so it gets value 0, otherwise lexer will break */
enum return_type {tEND_OF_FILE, tNAME, tLOOP, tLOOP_END, tID, tSEMICOLON,
                tDOUBLE_QUOTE, tSINGLE_QUOTE, tDATA, tDATALINE_BEGIN,
                tDATALINE, tDATALINE_END, tCOMMENT};  
 