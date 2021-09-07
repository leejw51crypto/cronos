


import pytest
from .conftest import setup_cronos, setup_chainmain

@pytest.fixture(scope="module")
def cronos(tmp_path_factory):
    print("########################################")
    print(tmp_path_factory)
    # "start-cronos"
    yield from setup_chainmain(tmp_path_factory.mktemp("chainmain"), 26700)



def test_ibc(cronos) :     
    assert True
    pass