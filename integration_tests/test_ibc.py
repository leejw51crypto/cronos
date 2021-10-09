import pytest
import time
import os
import json
from .conftest import setup_cronos2, setup_chainmain, setup_hermes
from web3 import Web3
import json
import sys


@pytest.fixture(scope="module")
def cronos(tmp_path_factory):
    print(f'cronos tmp folder= {tmp_path_factory}')
    yield from setup_cronos2(tmp_path_factory.mktemp("cronos"), 26700)


@pytest.fixture(scope="module")
def chainmain(tmp_path_factory):
    print(f'chainmain tmp folder= {tmp_path_factory}')
    # "start-cronos"
    yield from setup_chainmain(tmp_path_factory.mktemp("chainmain"), 26800)


@pytest.fixture(scope="module")
def hermes(tmp_path_factory):
    print("hermes waiting for chains booting up")
    time.sleep(20)
    print(f'hermes tmp folder= {tmp_path_factory}')
    yield from setup_hermes(tmp_path_factory.mktemp("hermes"), 26900)


def getBalance(chain, addr, denom):
    output = chain.cosmos_cli(0).raw(
        "query",
        "bank",
        "balances",
        addr,
        node=chain.node_rpc(0),
        output="json",
    )
    c = json.loads(output.decode())
    d = json.dumps(c, indent=4)
    print(d)
    coins = c["balances"]
    for coin in coins:
        if coin["denom"] == denom:
            value = int(coin["amount"])
            return value
    return 0


def test_ibc(cronos, chainmain, hermes):
    print("test ibc")
    time.sleep(2000000000)
    assert True
    pass
