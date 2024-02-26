import requests
import json
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starknet_py.net.models.chains import StarknetChainId

from collections import OrderedDict

RPC_mainnet = ""
RPC_devnet = "http://127.0.0.1:5050"

DEPLOYER_PRIV_KEY = "0x85de4dbfa077d7602041b1dfb751cee2"
DEPLOYER_ADDRESS = "0x11a9824a5fb6cbdad3ad776fb1117e11db1b28b041253b23abac50e1739aafc"

SELECTOR_CREATE_AND_INIT_POOL = "0x1e700c8df2b0c106c81e9b6e1089ccc00aa9da307295260672a7fd601029e93"
SELECTOR_MINT = "0x2f0b3c5710379609eb5495f1ecd348cb28167711b73609fe565a72734550354"
SELECTOR_APPROVE = "0x219209e083275171774dab1df80982e9df2096516f06319c5c6d71ae0a8480c"
SELECTOR_EXACT_INPUT_SINGLE = "0x8b15073164d9faa52b205fa2eecbf6004827f35a3730e91da3990d533ccfe8"
SELECTOR_COLLECT = "0x284134db6f39215e1d0a0a3dbd382fd7d28af6b3e3d5b77bba35c3a1d0da316"
SELECTOR_SWAP = "0x015543c3708653cda9d418b4ccd3be11368e40636c10c44b18cfe756b6d88b29"


STARKNET_ETH_TOKEN = '0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7'
STARKNET_USDC_TOKEN = '0x53c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8'
JEDI_POOL_ADDRESS = "0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a"
JEDI_FIRST_TX_HASH = "0x65e9e65b2090edfdb33ed7041f5c501488af52e8a94996939f46c4be7e20e6"
JEDI_NFT_MANAGER = "0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec"
JEDI_SWAP_MANAGER = "0x31a0c1ec4b27d0d0ce75a56b0d35d7ca79138aed511857627b33295b1175ffa"

dev_SWAP_ROUTER_ADDRESS = "0x4370d24f321619fe554307e1c2436f0e55735e968a8fe4cc5d3ae761d5d3c8b"
dev_NFT_ROUTER_ADDRESS = "0x20c52ca58d34335498df09c5766198ed97fbfbe0aeea4d8cd7c5e16e85724cb"
dev_ERC20_CONTRACT_ADDRESS = "0x73b196521e3ffc1972a9422d14de13841c4dffdbe6dea0db020ebdf6f05dae7"
dev_ETH_CONTRACT_ADDRESS = "0x49D36570D4E46F48E99674BD3FCC84644DDD6B96F7C741B1562B82F9E004DC7"

dev_POOL_ADDRESS = "0x3d77d30e4d58f30fcb3271e62f014a4bf8d6a8e8f0f5e1162dea77dfc4da0c7"


print("")


def get_starknet_events_data(rpc_node_url, contract_address, chunk_size, cont_token = None):
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "starknet_getEvents",
        "params": {
            "filter": {
                "from_block": {
                    "block_number": 0
                },
                "to_block": "latest",
                "address": contract_address,
                "keys": [[
                    
                ]],
                "continuation_token": cont_token,
                "chunk_size": chunk_size
            }
        },
    }

    response = requests.post(rpc_node_url, headers=headers, json=request_data)
    return response


def get_starknet_transaction_by_hash(rpc_node_url, tx_hash):
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "starknet_getTransactionByHash",
        "params": {
            "transaction_hash": tx_hash
        },
    }

    response = requests.post(rpc_node_url, headers=headers, json=request_data)
    return response

def add_starknet_invoke_transaction(account, call_datas, selector_list, contract_to_call):
    for i in range(len(call_datas)):
        call = Call(
            to_addr =contract_to_call[i],
            selector=selector_list[i],
            calldata=call_datas[i]
        )

        tx_response = account.execute_v1_sync(call, max_fee=12345678901234567890)
        print("tx_response ", i)
        print(tx_response)

#can be used to test create_and_init func
def create_and_init_pool(account): 
    call = Call(
        to_addr = int(dev_NFT_ROUTER_ADDRESS, 16),
        selector= int(SELECTOR_CREATE_AND_INIT_POOL, 16),
        calldata= [int(dev_ETH_CONTRACT_ADDRESS, 16), int(dev_ERC20_CONTRACT_ADDRESS, 16), 500, 3967682570592415043735410, 0] #token0, token1, fee, price
    )
    
    tx_response = account.execute_v1_sync(call, max_fee=12345678901234567890)
    print("create_and_init_pool tx_response:")
    print(tx_response)
    # first_mint(account)

# #should working?
# Replicates the call of the first Mint
def first_mint(account):
    call_list = []
    call = Call( #approve
        to_addr = int(dev_ETH_CONTRACT_ADDRESS, 16),
        selector= int(SELECTOR_APPROVE, 16),
        calldata= [int(dev_NFT_ROUTER_ADDRESS, 16), 31887432527575489, 0] #spender, amount
    )
    call_list.append(call)
    call = Call( #approve
        to_addr = int(dev_ERC20_CONTRACT_ADDRESS, 16),
        selector= int(SELECTOR_APPROVE, 16),
        calldata= [int(dev_NFT_ROUTER_ADDRESS, 16), 100000000, 0] #spender, amount
    )
    call_list.append(call)
    call = Call( #mint
        to_addr = int(dev_NFT_ROUTER_ADDRESS, 16),
        selector= int(SELECTOR_MINT, 16),
        calldata= [int(dev_ETH_CONTRACT_ADDRESS, 16), int(dev_ERC20_CONTRACT_ADDRESS, 16), int("0x1f4", 16), int("0x30e76", 16), int("0x1", 16), int("0x2fea4", 16), int("0x1", 16), int("0x714973709af317", 16), int("0x0", 16), int("0x5f5e100", 16), int("0x0", 16), int("0x6dfcc83c3cc78a", 16), int("0x0", 16), int("0x5d22923", 16), int("0x0", 16), int(DEPLOYER_ADDRESS, 16), int("0x65c7069f", 16)] #token0, token1, fee, tick_low, tick_up, amt0_desired, amt1_desired, amt0_min, amt1_min, recipient, deadline 
    )
    call_list.append(call)
    
    tx_response = account.execute_v1_sync(call_list, max_fee=12345678901234567890)
    print("first_mint tx_response:")
    print(tx_response)




## SETUP client & account
client_devnet = FullNodeClient(node_url=RPC_devnet)

key_pair = KeyPair.from_private_key(key=DEPLOYER_PRIV_KEY)
signer = StarkCurveSigner(DEPLOYER_ADDRESS, key_pair, StarknetChainId.GOERLI)
account_devnet = Account(client=client_devnet, address=DEPLOYER_ADDRESS, signer=signer)


## GET POOL TXS:
# events = get_starknet_events_data(RPC_mainnet, JEDI_POOL_ADDRESS, 3)
# events = json.loads(events.content.decode())["result"]
# Some hardcoded calls so that I dont make so many requests to rpc:
events = {'events': [{'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x3610d518bd9955fd50fcf99bc6982c4052fe12b8fa569e7452e678a4c657d59'], 'data': ['0x3483080cdae9803fecf72', '0x0', '0x305a0', '0x1'], 'block_number': 537870, 'block_hash': '0x87e51acc6df975db8ba885fe95b93eefd1230584917fdf3395e6aecf225001', 'transaction_hash': '0x65e9e65b2090edfdb33ed7041f5c501488af52e8a94996939f46c4be7e20e6'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x34e55c1cd55f1338241b50d352f0e91c7e4ffad0e4271d64eb347589ebdfd16'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x30e76', '0x1', '0x2fea4', '0x1', '0x10fbca607090', '0x714973709af317', '0x0', '0x5f5e100', '0x0'], 'block_number': 537870, 'block_hash': '0x87e51acc6df975db8ba885fe95b93eefd1230584917fdf3395e6aecf225001', 'transaction_hash': '0x65e9e65b2090edfdb33ed7041f5c501488af52e8a94996939f46c4be7e20e6'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0xe316f0d9d2a3affa97de1d99bb2aac0538e2666d0d8545545ead241ef0ccab'], 'data': ['0x31a0c1ec4b27d0d0ce75a56b0d35d7ca79138aed511857627b33295b1175ffa', '0x161a9bca8dcc5975a03b12f5f7bf9610e1541635eb40eb3a89baeedc168e636', '0x38d7ea4c68000', '0x0', '0x0', '0x262582', '0x0', '0x1', '0x345f18153b975ad84b34e', '0x0', '0x10fbca607090', '0x305d6', '0x1'], 'block_number': 538701, 'block_hash': '0x489c2fe20ab35da812df249a6b6141dfe4c5f6730a779a7e36c6da4b1d7c09e', 'transaction_hash': '0x2963401f55ac0890c5666b0c91bbbabd3cc6d1f717f9c6e445b0b60d824024'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x34e55c1cd55f1338241b50d352f0e91c7e4ffad0e4271d64eb347589ebdfd16'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x30ac0', '0x1', '0x2fea4', '0x1', '0x12a9cfde6a5ce', '0x8064cf6a7ce4974', '0x0', '0x3b9aca00', '0x0'], 'block_number': 539454, 'block_hash': '0x2824fdb38ae05cf22127f0047d1c13f54defd7dbe604a68e882d549e4272319', 'transaction_hash': '0x5766ef7c541ab34af1044eea09e1a10f728f23a073bbbcd835b54e1b83daa9'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x34e55c1cd55f1338241b50d352f0e91c7e4ffad0e4271d64eb347589ebdfd16'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x30ac0', '0x1', '0x2fea4', '0x1', '0x25539fbcd4b9d', '0x100c99ed4f9c99c8', '0x0', '0x77359400', '0x0'], 'block_number': 539464, 'block_hash': '0x411349b4b066c0fdb949a28475a10ce5b32576f6f0ec94f60c3de51f608a40e', 'transaction_hash': '0x7a2b33efe8856e6feb15300dd985d53c0ef499f47faf49d7a5272bc57c52b9f'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x243e1de00e8a6bc1dfa3e950e6ade24c52e4a25de4dee7fb5affe918ad1e744'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x30e76', '0x1', '0x2fea4', '0x1', '0x10fbca607090', '0x74d67dab0eeb16', '0x0', '0x5cfbb7d', '0x0'], 'block_number': 540321, 'block_hash': '0x15466bf1d55cf6a6c9b10059b95522ba5a5b2254debc5c43966cfbae575061e', 'transaction_hash': '0x6e9676c1b1d7afdd9bda17c802cf4aa9f408d20215eec7d90ac5348d9da154e'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x33b678d8846a558f55fc9257950e74c1aac32ee4c836c3a620d1066cc8d493f'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x161a9bca8dcc5975a03b12f5f7bf9610e1541635eb40eb3a89baeedc168e636', '0x30e76', '0x1', '0x2fea4', '0x1', '0x74d6f215617315', '0x5cfbb7d'], 'block_number': 540321, 'block_hash': '0x15466bf1d55cf6a6c9b10059b95522ba5a5b2254debc5c43966cfbae575061e', 'transaction_hash': '0x6e9676c1b1d7afdd9bda17c802cf4aa9f408d20215eec7d90ac5348d9da154e'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x243e1de00e8a6bc1dfa3e950e6ade24c52e4a25de4dee7fb5affe918ad1e744'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x30ac0', '0x1', '0x2fea4', '0x1', '0x25539fbcd4b9d', '0x100c99ed4f9c99c7', '0x0', '0x773593ff', '0x0'], 'block_number': 540325, 'block_hash': '0xcb5c83c4db718c5d2bf75b9722b8abb50c0eacd9da9732d51450472dee5251', 'transaction_hash': '0x4c994978cb1fcc7ddebd4d6a4e3993e7098262e8e5915cd014bbee18dbd82f6'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x33b678d8846a558f55fc9257950e74c1aac32ee4c836c3a620d1066cc8d493f'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x284a1ad6382cffc520d8f711cf9519ccf43b3c105b89ef081cbe1a625322410', '0x30ac0', '0x1', '0x2fea4', '0x1', '0x100c99ed4f9c99c7', '0x773593ff'], 'block_number': 540325, 'block_hash': '0xcb5c83c4db718c5d2bf75b9722b8abb50c0eacd9da9732d51450472dee5251', 'transaction_hash': '0x4c994978cb1fcc7ddebd4d6a4e3993e7098262e8e5915cd014bbee18dbd82f6'}, {'from_address': '0x508e297a3e1a9461c1f1a541dfff16c4a22e08238efe3b61c285c8da196ee3a', 'keys': ['0x243e1de00e8a6bc1dfa3e950e6ade24c52e4a25de4dee7fb5affe918ad1e744'], 'data': ['0x4d367b511dec42e5207c616e50afc8471ee8bdf53f46d1def9fc7d8411f1eec', '0x30ac0', '0x1', '0x2fea4', '0x1', '0x12a9cfde6a5ce', '0x8064cf6a7ce4973', '0x0', '0x3b9ac9ff', '0x0'], 'block_number': 540325, 'block_hash': '0xcb5c83c4db718c5d2bf75b9722b8abb50c0eacd9da9732d51450472dee5251', 'transaction_hash': '0x28c188d3f57e12cafcd4c5e207806a8429b75fbd122a4efca3171b237eadc90'}], 'continuation_token': '540325-305'}

events = events["events"]

tx_hashes = [event["transaction_hash"] for event in events]
tx_hashes = list(OrderedDict.fromkeys(tx_hashes)) #removes repeated values, since one tx can throw many events.

transactions = [get_starknet_transaction_by_hash(RPC_mainnet, tx_hash) for tx_hash in tx_hashes]
transactions = [json.loads(tx.content.decode())["result"] for tx in transactions]


## PARSE TX CALLDATA
calls = []
contract_to_call = []
selector_list = []
new_call = []
for tx in transactions:
    calldata = tx["calldata"]

    next_items = 0
    in_call_header = True
    new_call = []
    for item in calldata:
        if item == STARKNET_ETH_TOKEN:
            item = dev_ETH_CONTRACT_ADDRESS
        elif item == STARKNET_USDC_TOKEN:
            item = dev_ERC20_CONTRACT_ADDRESS
        elif item == JEDI_NFT_MANAGER:
            item = dev_NFT_ROUTER_ADDRESS
        elif item == JEDI_SWAP_MANAGER:
            item = dev_SWAP_ROUTER_ADDRESS
        elif item == JEDI_POOL_ADDRESS:
            item = dev_POOL_ADDRESS

        if in_call_header:
            if next_items == 0: #start call headers
                next_items = 2
                continue
            if next_items == 2: #is "to"
                contract_to_call.append(int(item, 16))
                next_items -= 1
                continue
            if next_items == 1: #is selector
                selector_list.append(int(item, 16))
                next_items -= 1
                in_call_header = False
                continue
        else:
            if next_items == 0: #start call body
                next_items = int(item, 16)
                continue
            if next_items > 0: #fill call body
                new_call.append(int(item, 16))
                # new_call.append(item) #use to debug, to view call_data in 0x format
                next_items -= 1
            if next_items == 0: #close call body
                # these modifications are bc some calls have variables that should be changed to devnets variables
                if selector_list[-1] == int(SELECTOR_APPROVE, 16):
                    new_call[0] = int(DEPLOYER_ADDRESS, 16)
                elif selector_list[-1] == int(SELECTOR_MINT, 16):
                    new_call[-2] = int(DEPLOYER_ADDRESS, 16)
                elif selector_list[-1] == int(SELECTOR_COLLECT):
                    new_call[1] = int(DEPLOYER_ADDRESS, 16)
                # elif selector_list[-1] == int(SELECTOR_SWAP, 16):
                # fibrous swap?
                elif selector_list[-1] == int(SELECTOR_EXACT_INPUT_SINGLE):
                    new_call[3] = int(DEPLOYER_ADDRESS, 16)

                calls.append(new_call)
                new_call = []
                in_call_header = True
                next_items = 2
    if len(calls) != len(selector_list) or len(calls) != len(contract_to_call):
        print("error in len(calls) or len(selector_list) or len(contract_to_call)")


# SEND TXs to devnet
add_starknet_invoke_transaction(account_devnet, calls, selector_list, contract_to_call)

# Check Emitted Events In Devnet
events = get_starknet_events_data(RPC_devnet, dev_POOL_ADDRESS, 3) 
events = json.loads(events.content.decode())["result"]
print(events)
exit()
