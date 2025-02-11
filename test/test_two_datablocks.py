import pytest
from pathlib import Path
from mmcifbuddy import ParserFlat

thedata = {}

@pytest.fixture(autouse=True, scope="session")
def get_dict():
    myparser = ParserFlat(verbose=False)
    cwd = Path(__file__).parent
    fnam = Path(cwd, "two_datablocks.cif")
    myparser.fopen(fnam)
    basedict = myparser.parse()
    thedata.update(basedict)
    myparser.fclose()
    yield thedata

# Tests here

def test_two_datablocks():
    assert 2 == len(thedata)

def test_entry_ids():
    assert "X987A" == thedata['data_X987A']['_entry.id']
    assert "T100A" == thedata['data_T100A']['_entry.id']
