#! /usr/bin/env python3

import os
import sys
import re
from pathlib import Path
from loguru import logger

logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm}</green> <level>{message}</level>")


# Update a version file with a version number of the form
# major.minor.micro. No letters allowed.

def get_version(path) -> str:

    with open(path) as f:
        for line in f.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                vers = line.split(delim)[1]
            else:
                logger.error(f"Unable to find version string in file {path}")
                raise SystemExit()
    if not re.match("\d+\.\d+\.\d+$", vers):
        logger.error(f"Version string in file {fnam} malformed: {vers}")
        raise SystemExit()

    return vers


def check_version_format(version):
    return re.match("\d+\.\d+\.\d+$", version)


def write_new_version_file(path, s) -> None:
    if not os.access(path, os.W_OK):
        logger.error("You have no write access to this file")
        raise SystemExit

    with open(path, 'w') as f:
        print(f"__version__ = '{s}'", file=f)


def updateversion(fname, major, minor, micro, new_version) -> None:
   
    if not fname.exists():
        logger.error(f"No such file: {fname}")
        raise SystemExit()
  
    if new_version:
        if not check_version_format(new_version):
            logger.error("Version number not of the form 1.2.3")
            raise SystemExit

        write_new_version_file(fname, new_version)
        logger.info(f"Setting version to {new_version}")
        return

    # If we continue, increase major, minor or micro version number

    vers = get_version(fname)
    new_version = [x for x in vers.split('.')]
    L = [int (x) for x in vers.split('.')] # integer version of vers
    
    if major:
        n = int(L[0]) + 1
        new_version[0] = str(n)
 
    if minor:
        n = int(L[1]) + 1
        new_version[1] = str(n)

    if micro:
        n = int(L[2]) + 1
        new_version[2] = str(n)

    new_version = '.'.join(new_version)
    write_new_version_file(fname, new_version)
    logger.info(f"This version {vers}, new version {new_version}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=Path) 
    parser.add_argument('--major',
                        action='store_true',
                        dest='major',
                        help='Increment major version'
                        )
    parser.add_argument('--minor',
                        action='store_true',
                        dest='minor',
                        help='Increment minor version'
                        )
    parser.add_argument('--micro',
                        action='store_true',
                        dest='micro',
                        help='Increment micro version'
                        )
    parser.add_argument('--set-version',
                    dest='new_version',
                    default=None,
                    help='Provide version of the form major.minor.micro',
                    type=str
                    )

    args = parser.parse_args()
    # If all arguments are false, set micro
    if not any([args.major, args.minor, args.micro]):
        args.micro = True

    args = vars(args)  # args is a Namespace object, convert to dict
    params = tuple(args.values()) # convert values to a tuple
 
    updateversion(*params) # * unpacks tuple
