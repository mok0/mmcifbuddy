import re


pat_int = re.compile(r"""
    ^-?   # optional minus sign
    \d+   # match a number
    $""", re.VERBOSE)


pat_float = re.compile(r"""
    ^  
    -?    # Optional minus sign
   (?:    # Start of the first non-capturing group:
    \d+   #  Match a number (integer part)
    ()    #  Match the empty string, capture in group 1
   )?     # Make the first non-capturing group optional
   (?:    # Start of the second non-capturing group:
    \.\d* #  Match a dot and an optional fractional part
    ()    #  Match the empty string, capture in group 2
   ){1}   # Make the second non-capturing group non-optional
   (?:    # Start of the third non-capturing group:
    e     #  Match an e or E
    -?    #  Match an optional minus sign
    \d+   #  Match a mandatory exponent
    ()    #  Match the empty string, capture in group 3
   )?     # Make the third non-capturing group optional
    $
  (?:     # Now make sure that at least the following groups participated:
   \2     #  Either group 2 (containing the empty string)
  |       # or
   \1\3   #  Groups 1 and 3 (because "1" or "e1" alone aren't valid matches)
  )""", re.IGNORECASE | re.VERBOSE)

pat_version = re.compile(r"^\d+\.\d+\.([\d+\.])*$")


def is_int(s: str) -> int | None:
    if re.match(pat_int, s):
        return int(s)
    return None

def is_float(s: str) -> float | None:
    # Make sure string contains numbers. This is needed because
    # float pattern fails on '.'
    if re.search(r"\d", s) is None:
        return None
    if re.match(pat_float, s):
        return float(s)
    return None

def is_version(s: str) -> bool:
    if re.match(pat_version, s):
        return True
    else:
        return False


def mmcif_convert(D: dict) -> None:

    for key, val in D.items():
        if not type(val) is list:
            raise TypeError(f"Data item {key} is not a list")
        
        convert_list(val)


def convert_list(val):

        for i, x in enumerate(val):

            if type(x) is list:
                if convert_list(x):
                    return True

            if type(x) is list:
                print("why did we get here?")
                raise SystemExit
            
            j = is_int(x)
            if j is not None:
                val[i] = j
                continue
            r = is_float(x)
            if r is not None:
                val[i] = r           
            #.
        #.
        return True
    #.
