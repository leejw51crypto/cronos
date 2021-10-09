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


def my_test(cronos, chainmain, hermes):
    print("test ibc")
    time.sleep(2000000000)
    assert True
    pass


def test_ibc(cronos, chainmain, hermes):
    # wait for hermes
    time.sleep(20)
    while True:
        print(f"test ibc config={hermes.configpath}")
        MYIBC0 = "chainmain-1"
        MYIBC1 = "cronos_777-1"
        MYCHANNEL = "channel-0"
        MYCONFIG = hermes.configpath
        # signer21
        RECEIVER = "crc1q04jewhxw4xxu3vlg3rc85240h9q7ns6hglz0g"
        SRCAMOUNT = 5
        SRCDENOM = "basecro"
        DSTDENOM = "basetcro"
        # dstchainid srcchainid srcportid srchannelid
        # chainmain-1 -> cronos_777-1
        cmd = f'hermes -c {MYCONFIG} tx raw ft-transfer {MYIBC1} {MYIBC0} transfer {MYCHANNEL} {SRCAMOUNT} -o 1000 -n 1 -d {SRCDENOM} -r {RECEIVER} -k testkey'
        print(f'hermes config= {MYCONFIG}')
        stream = os.popen(cmd)
        output = stream.read()
        print(output)
        dstaddr = f"{RECEIVER}"
        olddstbalance = getBalance(cronos, dstaddr, DSTDENOM)
        print(f"old balance={olddstbalance} denom={DSTDENOM}")
        time.sleep(5)
        newdstbalance = getBalance(cronos, dstaddr, DSTDENOM)
        print(f"new balance={newdstbalance} denom={DSTDENOM}")
        expectedbalance = olddstbalance + SRCAMOUNT*(10**10)
        assert expectedbalance == newdstbalance
        break
    assert True
    pass


def test_ibc_reverse(cronos, chainmain, hermes):
    # wait for hermes
    time.sleep(20)
    while True:
        print(f"test ibc config={hermes.configpath}")
        MYIBC0 = "chainmain-1"
        MYIBC1 = "cronos_777-1"
        MYCHANNEL = "channel-0"
        MYCONFIG = hermes.configpath
        # signer21
        RECEIVER = "cro1u08u5dvtnpmlpdq333uj9tcj75yceggszxpnsy"
        SRCAMOUNT = 2*(10**10)
        SRCDENOM = "basetcro"
        DSTDENOM = "ibc/6B5A664BF0AF4F71B2F0BAA33141E2F1321242FBD5D19762F541EC971ACB0865"
        # dstchainid srcchainid srcportid srchannelid
        # chainmain-1 <- cronos_777-1
        cmd = f'hermes -c {MYCONFIG} tx raw ft-transfer {MYIBC0} {MYIBC1} transfer {MYCHANNEL} {SRCAMOUNT} -o 1000 -n 1 -d {SRCDENOM} -r {RECEIVER} -k testkey'
        print(f'hermes config= {MYCONFIG}')
        stream = os.popen(cmd)
        output = stream.read()
        print(output)
        dstaddr = f"{RECEIVER}"
        olddstbalance = getBalance(chainmain, dstaddr, DSTDENOM)
        print(f"old balance={olddstbalance} denom={DSTDENOM}")
        time.sleep(5)
        newdstbalance = getBalance(chainmain, dstaddr, DSTDENOM)
        print(f"new balance={newdstbalance} denom={DSTDENOM}")
        expectedbalance = olddstbalance + SRCAMOUNT
        assert expectedbalance == newdstbalance
        break
    assert True
    pass


def test_contract(cronos, chainmain, hermes):
    CRONOS_NODE = 'http://127.0.0.1:26701'
    CRONOS_CHAINID = 777
    CRONOS_GAS = 3000000000
    CRONOS_MNEMONICS = "night renew tonight dinner shaft scheme domain oppose echo summer broccoli agent face guitar surface belt veteran siren poem alcohol menu custom crunch index"

    web3api = Web3(Web3.HTTPProvider(CRONOS_NODE))
    print(f'connected {web3api.isConnected()}')
    web3api.eth.account.enable_unaudited_hdwallet_features()
    account = web3api.eth.account.from_mnemonic(CRONOS_MNEMONICS)
    contractCreatorAddress = account.address
    contractCreatorBalance = web3api.eth.get_balance(contractCreatorAddress)
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
    bytecode = "608060405234801561001057600080fd5b506040518060400160405280600581526020017f48656c6c6f0000000000000000000000000000000000000000000000000000008152506000908051906020019061005c929190610062565b50610166565b82805461006e90610105565b90600052602060002090601f01602090048101928261009057600085556100d7565b82601f106100a957805160ff19168380011785556100d7565b828001600101855582156100d7579182015b828111156100d65782518255916020019190600101906100bb565b5b5090506100e491906100e8565b5090565b5b808211156101015760008160009055506001016100e9565b5090565b6000600282049050600182168061011d57607f821691505b6020821081141561013157610130610137565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b61055f806101756000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c8063a413686214610046578063cfae321714610062578063ef690cc014610080575b600080fd5b610060600480360381019061005b91906102eb565b61009e565b005b61006a6100b8565b604051610077919061036d565b60405180910390f35b61008861014a565b604051610095919061036d565b60405180910390f35b80600090805190602001906100b49291906101d8565b5050565b6060600080546100c790610443565b80601f01602080910402602001604051908101604052809291908181526020018280546100f390610443565b80156101405780601f1061011557610100808354040283529160200191610140565b820191906000526020600020905b81548152906001019060200180831161012357829003601f168201915b5050505050905090565b6000805461015790610443565b80601f016020809104026020016040519081016040528092919081815260200182805461018390610443565b80156101d05780601f106101a5576101008083540402835291602001916101d0565b820191906000526020600020905b8154815290600101906020018083116101b357829003601f168201915b505050505081565b8280546101e490610443565b90600052602060002090601f016020900481019282610206576000855561024d565b82601f1061021f57805160ff191683800117855561024d565b8280016001018555821561024d579182015b8281111561024c578251825591602001919060010190610231565b5b50905061025a919061025e565b5090565b5b8082111561027757600081600090555060010161025f565b5090565b600061028e610289846103b4565b61038f565b9050828152602081018484840111156102aa576102a9610509565b5b6102b5848285610401565b509392505050565b600082601f8301126102d2576102d1610504565b5b81356102e284826020860161027b565b91505092915050565b60006020828403121561030157610300610513565b5b600082013567ffffffffffffffff81111561031f5761031e61050e565b5b61032b848285016102bd565b91505092915050565b600061033f826103e5565b61034981856103f0565b9350610359818560208601610410565b61036281610518565b840191505092915050565b600060208201905081810360008301526103878184610334565b905092915050565b60006103996103aa565b90506103a58282610475565b919050565b6000604051905090565b600067ffffffffffffffff8211156103cf576103ce6104d5565b5b6103d882610518565b9050602081019050919050565b600081519050919050565b600082825260208201905092915050565b82818337600083830152505050565b60005b8381101561042e578082015181840152602081019050610413565b8381111561043d576000848401525b50505050565b6000600282049050600182168061045b57607f821691505b6020821081141561046f5761046e6104a6565b5b50919050565b61047e82610518565b810181811067ffffffffffffffff8211171561049d5761049c6104d5565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f830116905091905056fea2646970667358221220083586d0f8cd8229b9095e03867043b89dbaa975ae534871f1da6e7168e84e4064736f6c63430008070033"
    abistring = '[{"inputs": [], "stateMutability": "nonpayable", "type": "constructor"}, {"inputs": [], "name": "greet", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "greeting", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "string", "name": "_greeting", "type": "string"}], "name": "setGreeting", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
    abi = json.loads(abistring)
    print(f'bytecode={bytecode}')
    print(f'abi={json.dumps(abistring)}')
    web3api.eth.defaultAccount = account
    # deploy
    greeterContractClass = web3api.eth.contract(abi=abi, bytecode=bytecode)
    nonce = web3api.eth.get_transaction_count(account.address)
    info = {'from': account.address, 'nonce': nonce,
            'gas': CRONOS_GAS, 'chainId': CRONOS_CHAINID}
    print(
        f"account= {contractCreatorAddress} balance= {contractCreatorBalance} nonce={nonce}")
    print(f'nonce= {nonce}')
    txhash = greeterContractClass.constructor().transact(info)
    print(f'txhash = {txhash.hex()}')
    txreceipt = web3api.eth.wait_for_transaction_receipt(txhash)
    print(f"txreceipt= {txreceipt}")

    # call contract
    greeterContractInstance = web3api.eth.contract(
        address=txreceipt.contractAddress,
        abi=abi
    )
    print(f"contract adddress= {txreceipt.contractAddress}")
    greeterCallResult = greeterContractInstance.functions.greet().call(info)
    print(f'result={greeterCallResult}')

    # change
    nonce = web3api.eth.get_transaction_count(account.address)
    info['nonce'] = nonce
    txhash = greeterContractInstance.functions.setGreeting('world').transact(info)
    txreceipt = web3api.eth.wait_for_transaction_receipt(txhash)
    print(f"txreceipt={txreceipt}")

    # call contract
    greeterCallResult = greeterContractInstance.functions.greet().call(info)
    print(f'contract call result={greeterCallResult}')
    assert "world" == greeterCallResult
    pass
