#! /usr/bin/env python3
## This script generates a version.h file for the mmciflexermodule

import subprocess
from pathlib import Path
import mmcifbuddy
from mmcifbuddy.logger import logger


def write_version_h() -> None:

    source = Path.cwd() / "src/mmciflexermodule.c"
    if not source.exists():
        logger.error("mmciflexermodule.c not found where expected")
        raise SystemExit

    p = Path.cwd()  / "src/version.h"
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

    # Get the version number from the mmcifbuddy module
    version = mmcifbuddy.__version__
    if version:
        print(f"#define VERSION \"{version}\"", file=outf)

    outf.close()


if __name__ == "__main__":

    write_version_h()
