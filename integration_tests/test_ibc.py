import pytest
from .conftest import setup_cronos, setup_chainmain

@pytest.fixture(scope="module")
def cronos(tmp_path_factory):    
    print(f'cronos tmp folder= {tmp_path_factory}')
    yield from setup_cronos(tmp_path_factory.mktemp("cronos"), 26700)

@pytest.fixture(scope="module")
def chainmain(tmp_path_factory):    
    print(f'chainmain tmp folder= {tmp_path_factory}')
    # "start-cronos"
    yield from setup_chainmain(tmp_path_factory.mktemp("chainmain"), 26800)

def test_ibc(chainmain, cronos) :     
    assert True
    pass