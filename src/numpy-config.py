#! /usr/bin/env python3

import numpy as np
import sys
from pathlib import Path


numpy_include_path = Path(np.get_include())
arrayobject_h = numpy_include_path / 'numpy' /'arrayobject.h'

if arrayobject_h.exists():
    print(f"-I{numpy_include_path}") 
else:
    print('arrayobject.h not found :-()')
