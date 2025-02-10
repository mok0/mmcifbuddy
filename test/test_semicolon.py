import pytest
from pathlib import Path
from mmcifbuddy.parser import Parser

thedata = {}

@pytest.fixture(autouse=True, scope="session")
def get_dict():
    myparser = Parser()
    cwd = Path(__file__).parent
    fnam = Path(cwd, "semicolon.cif")
    myparser.fopen(fnam)
    _ = myparser.parse()
    thedata.update(myparser.get_dict())
    myparser.fclose()
    yield thedata

# Tests here

def test_semicolon_test():
    assert 6 == len(thedata['_semicolon']['test'])

def test_exptl_crystal():

    text = """Author collected the first dataset in the dark, then a second dataset was
collected on the same crystal after inducing a photostationary state with
continuous illumination. The structure was refined by the application of
difference refinement to both datasets.""".split('\n')
    assert 4 == len(thedata['_exptl_crystal']['description'])

    for i, line in enumerate(thedata['_exptl_crystal']['description']):
        assert text[i] == line
