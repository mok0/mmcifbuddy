
enum return_type {ZERO, tNAME, tLOOP, tLOOP_END, tID, tSEMICOLON,
                tDOUBLE_QUOTE, tSINGLE_QUOTE, tDATA, tDATALINE_BEGIN,
                tDATALINE, tDATALINE_END, tCOMMENT};      /* ZERO must be first, it's never used */
 
#ifdef WANT_RETURN_TYPES
char *return_type_name[] = {"ZERO","tNAME","tLOOP", "tLOOP_END", "tID","tSEMICOLON",
                             "tDOUBLE_QUOTE", "tSINGLE_QUOTE", "tDATA",
                            "tDATALINE_BEGIN", "tDATALINE", "tDATALINE_END", "tCOMMENT"};
#endif
