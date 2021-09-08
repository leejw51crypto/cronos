import json
import os
import time

import pytest
from web3 import Web3

from .network import setup_chainmain, setup_cronos2, setup_hermes


@pytest.fixture(scope="module")
def cronos(tmp_path_factory):
    yield from setup_cronos2(tmp_path_factory.mktemp("cronos"), 26700)


@pytest.fixture(scope="module")
def chainmain(tmp_path_factory):
    # "start-cronos"
    yield from setup_chainmain(tmp_path_factory.mktemp("chainmain"), 26800)


@pytest.fixture(scope="module")
def hermes(tmp_path_factory):
    time.sleep(20)
    yield from setup_hermes(tmp_path_factory.mktemp("hermes"), 26900)


def get_balance(chain, addr, denom):
    output = chain.cosmos_cli(0).raw(
        "query",
        "bank",
        "balances",
        addr,
        node=chain.node_rpc(0),
        output="json",
    )
    c = json.loads(output.decode())
    coins = c["balances"]
    for coin in coins:
        if coin["denom"] == denom:
            value = int(coin["amount"])
            return value
    return 0


def test_ibc(cronos, chainmain, hermes):
    # wait for hermes
    time.sleep(20)
    while True:
        my_ibc0 = "chainmain-1"
        my_ibc1 = "cronos_777-1"
        my_channel = "channel-0"
        my_config = hermes.configpath
        # signer21
        coin_receiver = "crc1q04jewhxw4xxu3vlg3rc85240h9q7ns6hglz0g"
        src_amount = 5
        src_denom = "basecro"
        dst_denom = "basetcro"
        # dstchainid srcchainid srcportid srchannelid
        # chainmain-1 -> cronos_777-1
        cmd = f"hermes -c {my_config} tx raw ft-transfer \
        {my_ibc1} {my_ibc0} transfer {my_channel} {src_amount} \
        -o 1000 -n 1 -d {src_denom} -r {coin_receiver} -k testkey"
        os.popen(cmd)
        dstaddr = f"{coin_receiver}"
        olddstbalance = get_balance(cronos, dstaddr, dst_denom)
        time.sleep(5)
        newdstbalance = get_balance(cronos, dstaddr, dst_denom)
        expectedbalance = olddstbalance + src_amount * (10 ** 10)
        assert expectedbalance == newdstbalance
        break
    assert True
    pass


def test_ibc_reverse(cronos, chainmain, hermes):
    # wait for hermes
    time.sleep(20)
    while True:
        my_ibc0 = "chainmain-1"
        my_ibc1 = "cronos_777-1"
        my_channel = "channel-0"
        my_config = hermes.configpath
        # signer21
        coin_receiver = "cro1u08u5dvtnpmlpdq333uj9tcj75yceggszxpnsy"
        src_amount = 2 * (10 ** 10)
        src_denom = "basetcro"
        dst_denom = "ibc/6B5A664BF0AF4F71B2F0BAA33141E2F1321242FBD\
5D19762F541EC971ACB0865"
        # dstchainid srcchainid srcportid srchannelid
        # chainmain-1 <- cronos_777-1
        cmd = f"hermes -c {my_config} tx raw ft-transfer \
        {my_ibc0} {my_ibc1} transfer {my_channel} {src_amount} \
        -o 1000 -n 1 -d {src_denom} -r {coin_receiver} -k testkey"
        os.popen(cmd)
        dstaddr = f"{coin_receiver}"
        olddstbalance = get_balance(chainmain, dstaddr, dst_denom)
        time.sleep(5)
        newdstbalance = get_balance(chainmain, dstaddr, dst_denom)
        expectedbalance = olddstbalance + src_amount
        assert expectedbalance == newdstbalance
        break
    assert True
    pass


def test_contract(cronos, chainmain, hermes):
    cronos_node = "http://127.0.0.1:26701"
    cronos_chainid = 777
    cronos_gas = 3000000000
    cronos_mnemonics = "night renew tonight dinner shaft scheme \
domain oppose echo summer broccoli agent face guitar surface \
belt veteran siren poem alcohol menu custom crunch index"
    web3api = Web3(Web3.HTTPProvider(cronos_node))
    web3api.eth.account.enable_unaudited_hdwallet_features()
    account = web3api.eth.account.from_mnemonic(cronos_mnemonics)
    contract_creator_address = account.address
    web3api.eth.get_balance(contract_creator_address)
    """
    #install_solc(version='latest')
    #compiled_sol = compile_source(
        pragma solidity >0.5.0;

        contract Greeter {
            string public greeting;

            constructor() public {
                greeting = 'Hello';
            }

            function setGreeting(string memory _greeting) public {
                greeting = _greeting;
            }

            function greet() view public returns (string memory) {
                return greeting;
            }
        }
    # prepare contract
    #contract_id, contract_interface = compiled_sol.popitem()
    #bytecode = contract_interface['bin']
    #abi = contract_interface['abi']
    """

    # precompiled contract
    bytecode = (
        "608060405234801561001057600080fd5b50604051806040016040528060"
        "0581526020017f48656c6c6f000000000000000000000000000000000000"
        "0000000000000000008152506000908051906020019061005c9291906100"
        "62565b50610166565b82805461006e90610105565b906000526020600020"
        "90601f01602090048101928261009057600085556100d7565b82601f1061"
        "00a957805160ff19168380011785556100d7565b82800160010185558215"
        "6100d7579182015b828111156100d6578251825591602001919060010190"
        "6100bb565b5b5090506100e491906100e8565b5090565b5b808211156101"
        "015760008160009055506001016100e9565b5090565b6000600282049050"
        "600182168061011d57607f821691505b6020821081141561013157610130"
        "610137565b5b50919050565b7f4e487b7100000000000000000000000000"
        "000000000000000000000000000000600052602260045260246000fd5b61"
        "055f806101756000396000f3fe608060405234801561001057600080fd5b"
        "50600436106100415760003560e01c8063a413686214610046578063cfae"
        "321714610062578063ef690cc014610080575b600080fd5b610060600480"
        "360381019061005b91906102eb565b61009e565b005b61006a6100b8565b"
        "604051610077919061036d565b60405180910390f35b61008861014a565b"
        "604051610095919061036d565b60405180910390f35b8060009080519060"
        "2001906100b49291906101d8565b5050565b6060600080546100c7906104"
        "43565b80601f016020809104026020016040519081016040528092919081"
        "81526020018280546100f390610443565b80156101405780601f10610115"
        "57610100808354040283529160200191610140565b820191906000526020"
        "600020905b81548152906001019060200180831161012357829003601f16"
        "8201915b5050505050905090565b6000805461015790610443565b80601f"
        "016020809104026020016040519081016040528092919081815260200182"
        "805461018390610443565b80156101d05780601f106101a5576101008083"
        "540402835291602001916101d0565b820191906000526020600020905b81"
        "54815290600101906020018083116101b357829003601f168201915b5050"
        "50505081565b8280546101e490610443565b90600052602060002090601f"
        "016020900481019282610206576000855561024d565b82601f1061021f57"
        "805160ff191683800117855561024d565b8280016001018555821561024d"
        "579182015b8281111561024c578251825591602001919060010190610231"
        "565b5b50905061025a919061025e565b5090565b5b808211156102775760"
        "0081600090555060010161025f565b5090565b600061028e610289846103"
        "b4565b61038f565b9050828152602081018484840111156102aa576102a9"
        "610509565b5b6102b5848285610401565b509392505050565b600082601f"
        "8301126102d2576102d1610504565b5b81356102e284826020860161027b"
        "565b91505092915050565b60006020828403121561030157610300610513"
        "565b5b600082013567ffffffffffffffff81111561031f5761031e61050e"
        "565b5b61032b848285016102bd565b91505092915050565b600061033f82"
        "6103e5565b61034981856103f0565b935061035981856020860161041056"
        "5b61036281610518565b840191505092915050565b600060208201905081"
        "810360008301526103878184610334565b905092915050565b6000610399"
        "6103aa565b90506103a58282610475565b919050565b6000604051905090"
        "565b600067ffffffffffffffff8211156103cf576103ce6104d5565b5b61"
        "03d882610518565b9050602081019050919050565b600081519050919050"
        "565b600082825260208201905092915050565b8281833760008383015250"
        "5050565b60005b8381101561042e57808201518184015260208101905061"
        "0413565b8381111561043d576000848401525b50505050565b6000600282"
        "049050600182168061045b57607f821691505b6020821081141561046f57"
        "61046e6104a6565b5b50919050565b61047e82610518565b810181811067"
        "ffffffffffffffff8211171561049d5761049c6104d5565b5b8060405250"
        "5050565b7f4e487b71000000000000000000000000000000000000000000"
        "00000000000000600052602260045260246000fd5b7f4e487b7100000000"
        "000000000000000000000000000000000000000000000000600052604160"
        "045260246000fd5b600080fd5b600080fd5b600080fd5b600080fd5b6000"
        "601f19601f830116905091905056fea2646970667358221220083586d0f8"
        "cd8229b9095e03867043b89dbaa975ae534871f1da6e7168e84e4064736f"
        "6c63430008070033"
    )

    abistring = (
        '[{"inputs": [], "stateMutability": "nonpayable", "type": "co'
        'nstructor"}, {"inputs": [], "name": "greet", "outputs": [{"i'
        'nternalType": "string", "name": "", "type": "string"}], "sta'
        'teMutability": "view", "type": "function"}, {"inputs": [], "'
        'name": "greeting", "outputs": [{"internalType": "string", "n'
        'ame": "", "type": "string"}], "stateMutability": "view", "ty'
        'pe": "function"}, {"inputs": [{"internalType": "string", "na'
        'me": "_greeting", "type": "string"}], "name": "setGreeting",'
        ' "outputs": [], "stateMutability": "nonpayable", "type": "fu'
        'nction"}]'
    )

    abi = json.loads(abistring)
    web3api.eth.defaultAccount = account
    # deploy
    greeter_contract_class = web3api.eth.contract(abi=abi, bytecode=bytecode)
    nonce = web3api.eth.get_transaction_count(account.address)
    info = {
        "from": account.address,
        "nonce": nonce,
        "gas": cronos_gas,
        "chainId": cronos_chainid,
    }
    txhash = greeter_contract_class.constructor().transact(info)
    txreceipt = web3api.eth.wait_for_transaction_receipt(txhash)

    # call contract
    greeter_contract_instance = web3api.eth.contract(
        address=txreceipt.contractAddress, abi=abi
    )
    greeter_call_result = greeter_contract_instance.functions.greet().call(info)

    # change
    nonce = web3api.eth.get_transaction_count(account.address)
    info["nonce"] = nonce
    txhash = greeter_contract_instance.functions.setGreeting("world").transact(info)
    web3api.eth.wait_for_transaction_receipt(txhash)

    # call contract
    greeter_call_result = greeter_contract_instance.functions.greet().call(info)
    assert "world" == greeter_call_result
    pass
