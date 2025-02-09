import logging

def theformat(col) -> str:
    reset = "\x1b[0m"
    long_format = f"\x1b[36;20m%(asctime)s [{col}%(levelname)s{reset}] %(message)s"
    short_format = f"[{col}%(levelname)s{reset}] %(message)s"
    return long_format


class CustomFormatter(logging.Formatter):
    yellow = "\x1b[33;20m"
    green = "\x1b[32;20m"
    red = "\x1b[31;20m"
    magenta = '\x1b[35m'
    bold_red = "\x1b[31;1m"

    FORMATS = {
        logging.DEBUG: theformat(magenta),
        logging.INFO: theformat(green),
        logging.WARNING: theformat(yellow),
        logging.ERROR: theformat(red),
        logging.CRITICAL: theformat(bold_red)
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        #long_dateformat = '%Y-%m-%d %H:%M %Z'
        long_dateformat = '%Y-%m-%d %H:%M'
        short_dateformat = '%H:%M'
        #formatter = logging.Formatter(log_fmt,  datefmt=short_dateformat)
        formatter = logging.Formatter(log_fmt,  datefmt=long_dateformat)
        return formatter.format(record)

logger = logging.getLogger("install_ng")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

if __name__ == "__main__":
    logger.debug("This is debug info")
    logger.info("This is some info")
    logger.warning("There was a warning")
    logger.error("There was an error!")
    logger.critical("This is CRITICAL!")
