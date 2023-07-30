#! /usr/bin/env python3

# This script generates a version.h file for the mmciflexermodule

import sys
import subprocess
from pathlib import Path
from loguru import logger

logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm}</green> <level>{message}</level>")

def create_version() -> None:

    source = Path.cwd() / "mmciflexermodule.c"
    if not source.exists():
        logger.error("mmciflexermodule.c not found where expected")
        raise SystemExit

    p = Path.cwd()  / "version.h"
    outf = p.open('w')

    try:
        git_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                    capture_output=True, text=True, check=True)
        git_commit = git_commit.stdout.strip()
        print(f"#define GIT_COMMIT \"{git_commit}\"", file=outf)
    except subprocess.CalledProcessError:
        print("#define GIT_COMMIT \"None\"", file=outf)

    try:
        git_branch = subprocess.run(["git", "branch", "--show-current"],
                                    capture_output=True, text=True, check=True)
        git_branch = git_branch.stdout.strip()
        print(f"#define GIT_BRANCH \"{git_branch}\"", file=outf)
    except subprocess.CalledProcessError:
        print("#define GIT_BRANCH \"None\"", file=outf)


    compile_time = subprocess.run(['date', '-u', "+'%Y-%m-%d %H:%M:%S UTC'"],
                                capture_output=True, text=True, check=True)
    compile_time = compile_time.stdout.strip().replace("'", '')
    print(f"#define COMPILE_TIME \"{compile_time}\"", file=outf)

    outf.close()

    logger.info(f"Wrote new file {p}")


if __name__ == "__main__":

    create_version()
