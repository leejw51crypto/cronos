import pytest
import time
import os
import json
from .conftest import setup_cronos2, setup_chainmain, setup_hermes

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
    print("hermes waiting~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
    time.sleep(20) 
    print(f'chainmain tmp folder= {tmp_path_factory}')
    # "start-cronos"
    yield from setup_hermes(tmp_path_factory.mktemp("hermes"), 26900)


def getBalance(chain,addr,denom):
    output = chain.cosmos_cli(0).raw (    
        "query",
        "bank",
        "balances",
        addr,
        node=chain.node_rpc(0),
        output="json",
    )
    c=json.loads(output.decode())
    d=json.dumps(c, indent=4)
    print(d)
    coins= c["balances"]
    for coin in coins:
        if coin["denom"]==denom :
            value=int(coin["amount"])
            return value
    return 0
    
def my_ibc2(cronos,chainmain, hermes) :   
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@ testibc")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # wait for hermes    
    time.sleep(20) 
    while True:
        print("~~~~~~~~~~~~")      
        print(f"test ibc config2={hermes.configpath}")       
        time.sleep(500000)
    pass
        
  
def test_ibc(cronos,chainmain, hermes) :   
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@ testibc")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # wait for hermes    
    time.sleep(20) 
    while True:
        print("###########################################")      
        print(f"test ibc config={hermes.configpath}")
        MYIBC0="chainmain-1"
        MYIBC1="cronos_777-1"
        MYCHANNEL="channel-0"
        MYCONFIG=hermes.configpath
        RECEIVER="ethm1q04jewhxw4xxu3vlg3rc85240h9q7ns6mctk75"
        # dstchanid srcchainid srcportid srchannelid
        cmd=f'hermes -c {MYCONFIG} tx raw ft-transfer {MYIBC1} {MYIBC0} transfer {MYCHANNEL} 2 -o 1000 -n 1 -d basecro -r {RECEIVER} -k testkey'
        print(f'##########     {cmd}')
        stream = os.popen(cmd)
        output = stream.read()
        print(output)
        addr = f"{RECEIVER}"
        DENOM="ibc/6411AE2ADA1E73DB59DB151A8988F9B7D5E7E233D8414DB6817F8F1A01611F86"
        oldbalance= getBalance(cronos, addr, DENOM)
        print(f"oldbalance={oldbalance}")
        time.sleep(5)
        newbalance= getBalance(cronos, addr, DENOM)
        print(f"newbalance={newbalance}")
        assert oldbalance + 2 == newbalance        
        time.sleep(500000)        
        break    
    assert True
    pass