#! /usr/bin/env python3

# This script generates a version.h file for the mmciflexermodule

import subprocess
from pathlib import Path


p = Path.cwd()  / "version.h"

git_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], 
                          capture_output=True, text=True, check=True)
git_branch = subprocess.run(["git", "branch", "--show-current"],
                              capture_output=True, text=True, check=True)
compile_time = subprocess.run(['date', '-u', "+'%Y-%m-%d %H:%M:%S UTC'"],
                              capture_output=True, text=True, check=True)

git_commit = git_commit.stdout.strip()
git_branch = git_branch.stdout.strip()
compile_time = compile_time.stdout.strip().replace("'", '')

with open(p, 'w') as outf:
    print(f"#define GIT_COMMIT \"{git_commit}\"", file=outf)
    print(f"#define GIT_BRANCH \"{git_branch}\"", file=outf)
    print(f"#define COMPILE_TIME \"{compile_time}\"", file=outf)

print(f"Wrote new file {p}")
