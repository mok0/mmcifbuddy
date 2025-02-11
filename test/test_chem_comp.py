import pytest
from pathlib import Path
from mmcifbuddy.parser import Parser

thedata = {}

@pytest.fixture(autouse=True, scope="session")
def get_dict():
    myparser = Parser(verbose=False)
    cwd = Path(__file__).parent
    fnam = Path(cwd, "chem_comp.cif")
    myparser.fopen(fnam)
    _ = myparser.parse()
    thedata.update(myparser.get_dict())
    myparser.fclose()
    yield thedata

# Tests here

def test_chem_comp():
    assert 7 == len(thedata['_chem_comp'])

    # for k, v in thedata['_chem_comp'].items():
    #     print("***", k)
    #     print( v)
    #     print(20*"-")
