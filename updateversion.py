import sys
import re
from loguru import logger

logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm}</green> <level>{message}</level>")


# Update a version file with a version number of the form
# major.minor.micro. No letters allowed.

def get_version(path):

    with open(path) as f:
        for line in f.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                vers = line.split(delim)[1]
            else:
                raise RuntimeError("Unable to find version string.")
    if not re.match("\d+\.\d+\.\d+$", vers):
        logger.error(f"Version string in file {fnam} malformed: {vers}")
        raise SystemExit()

    return vers

def increase_micro(ver):
    vers = ver.split('.')
    n = int(vers[2]) + 1
    vers[2] = str(n)
    return '.'.join(vers)

def increase_minor(ver):
    vers = ver.split('.')
    n = int(vers[1]) + 1
    vers[1] = str(n)
    return '.'.join(vers)

def increase_major(ver):
    vers = ver.split('.')
    n = int(vers[0]) + 1
    vers[0] = str(n)
    return '.'.join(vers)


def write_new_version_file(path, s):
    with open(path, 'w') as f:
        print(f"__version__ = '{s}'", file=f)


if __name__ == "__main__":
    from pathlib import Path

    fnam = Path(sys.argv[1])

    if not fnam.exists():
        raise SystemExit("No such file")

    vers = get_version(fnam)
    new_vers = increase_micro(vers)
    logger.info(f"This version {vers}, new version {new_vers}")
    write_new_version_file(fnam, new_vers)
