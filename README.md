# Starknet JediSwap Transaction Replicator
This project replicates on a local starknet-devnet blockchain transactions that occurred on starknet-mainnet.

This was implemented to simulate an error case found on JediSwap V2 Mainnet. The idea is to replicate locally the transactions that ocurred on a specific pool to try to achieve the same errored state on a local devnet.

Disclaimer: I, me, or we, can't and won't be held responsable for any business decision, or any other type of decision, made resulting from the behaviour of this project. This project is experimental, use at your own risk.

## Requirements
- [Starknet-py](https://starknetpy.readthedocs.io/en/latest/installation.html)
- [Starknet-devnet](https://github.com/0xSpaceShard/starknet-devnet-rs)
- [Starkli](https://github.com/xJonathanLEI/starkli)
- [starknet-foundry](https://github.com/foundry-rs/starknet-foundry)
- [JediSwap V2 Core Contracts](https://github.com/jediswaplabs/JediSwap-v2-core/)
- [JediSwap V2 Periphery Contracts](https://github.com/jediswaplabs/JediSwap-v2-periphery)


## Setup devnet
### 1. Start local devnet

```bash
starknet-devnet --seed 104406940 
```
TODO: add param that stores devnet state on exit

**Note**: 
- If this seed is used, most addresses configured in this repo should work
- Another highly recommended paramenter combination is: 
    - --dump-on <ACTION_>
        - Specify when to dump the state of Devnet (possible values: exit, transaction)
    - --dump-path <DUMP_PATH>
        - Specify the path to dump to

From this devnet we will be using the first prefunded address as our deployer:

- Account address:
    - 0x11a9824a5fb6cbdad3ad776fb1117e11db1b28b041253b23abac50e1739aafc 
- Private key:
    - 0x85de4dbfa077d7602041b1dfb751cee2
- Public key:
    - 0x2d8c8094b44e076e71ed41b25d3c3b520f10c195bc8d0d1bf8853bdcf025d1a

### 2. Configure devnet

[Create an Account](https://docs.starknet.io/documentation/quick_start/set_up_an_account/#creating_a_keystore_file)

You may use the [provided account file](account_jedi.json) to interact with the blockchains while using sncast or starkli.

We will then need to add the newly generated account to the devnet:
```bash
sncast \
    --url http://127.0.0.1:5050 \
    account add \
    --name Jedi \
    --address 0x11a9824a5fb6cbdad3ad776fb1117e11db1b28b041253b23abac50e1739aafc \
    --private-key 0x85de4dbfa077d7602041b1dfb751cee2 \
    --class-hash 0x4d07e40e93398ed3c76981e72dd1fd22557a78ce36c0515f679e27f0bb5bc5f \
    --deployed
```
## Setup Contracts
### 1. Deploy [Factory](https://github.com/jediswaplabs/JediSwap-v2-core/blob/main/src/jediswap_v2_factory.cairo)
To deploy our Pool Factory we will need to run the following script from [JediSwap V2 Core Contracts](https://github.com/jediswaplabs/JediSwap-v2-core/)
```bash
sncast --url http://127.0.0.1:5050 --account Jedi --path-to-scarb-toml scripts/Scarb.toml script deploy_factory_and_pool
```

This will output a message similar to the following:
```bash
('Factory Deployed to ')
[DEBUG]	0x1909361eb66abb54210fab711c698486eb6d9a18800b11cdb49823c62207337
```

**Note**: We will need to save this address for future usage.

### 2. Deploy ERC20
So that we can create a pool to swap ETH and USDC, we need to deploy an ERC20 to simulate the USDC locally. For this we may:
```bash
starkli declare --account account_jedi.json --private-key 0x85de4dbfa077d7602041b1dfb751cee2 --watch ERC20.contract_class.json --rpc http://127.0.0.1:5050
```

This should output a message similar to the following:
```bash
Class hash declared:
0x049ba5c980cc15723e123bf55c6863526145d20812d10e7c02132aade13f9c4e
```

We will then need to deploy the erc20
```bash
deploy erc20:
starkli deploy \
    --watch 0x049ba5c980cc15723e123bf55c6863526145d20812d10e7c02132aade13f9c4e \
    1970496611 \
    1970496611 \
    u256:4000000000000000000000 \
    0x11a9824a5fb6cbdad3ad776fb1117e11db1b28b041253b23abac50e1739aafc \
    --rpc http://127.0.0.1:5050 \
    --account account_jedi.json --private-key 0x85de4dbfa077d7602041b1dfb751cee2
```

Which should give an output similar to the following:
```bash
Contract deployed:
0x073b196521e3ffc1972a9422d14de13841c4dffdbe6dea0db020ebdf6f05dae7
```

**Note**: remember to save this address as we will need it later.

### 3. Deploy [Periphery Contracts](https://github.com/jediswaplabs/JediSwap-v2-periphery)

For the following we will need the nonce of the deployer address
```bash
curl --location '127.0.0.1:5050' \ --header 'Content-Type: application/json' \ --data '{"jsonrpc":"2.0","id":1,"method":"starknet_getNonce","params":{"block_id": "latest", "contract_address": "0x11a9824a5fb6cbdad3ad776fb1117e11db1b28b041253b23abac50e1739aafc"}}'
```

Then we will need to set thr deployer's address nonce, and the factory contract address in [the following file](https://github.com/jediswaplabs/JediSwap-v2-periphery/blob/main/scripts/src/deploy_routers.cairo). Then run the follwoing script from [JediSwap's Periphery Contracts](https://github.com/jediswaplabs/JediSwap-v2-periphery/):
```bash
sncast --url http://127.0.0.1:5050 --account Jedi --path-to-scarb-toml scripts/Scarb.toml script deploy_routers
```

Which should output somethiing similar to the following:
```bash
('NFT Manager Deployed to ') (for mints, burns, collects)
[DEBUG]	0x20c52ca58d34335498df09c5766198ed97fbfbe0aeea4d8cd7c5e16e85724cb

('Swap Router Deployed to ') (for swaps)
[DEBUG]	0x4370d24f321619fe554307e1c2436f0e55735e968a8fe4cc5d3ae761d5d3c8b
```
**Note**: Again, dont forget to store this both addresses.

### 4. Create and init pool

Having the previous smart contracts, now we should deploy a Pool, consisting of the preset ETH address granted by devnet + the deployed ERC20.
To deploy the pool you should run the following command:
```bash
starkli call \
   0x20c52ca58d34335498df09c5766198ed97fbfbe0aeea4d8cd7c5e16e85724cb \
   create_and_initialize_pool \
   0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7 \
   0x073b196521e3ffc1972a9422d14de13841c4dffdbe6dea0db020ebdf6f05dae7 \
   0x1f4 \
   0x3483080cdae9803fecf72 \
   0x0 \
   --rpc http://127.0.0.1:5050 
```

Which should output the created pool address:
```bash
pool address:
0x03d77d30e4d58f30fcb3271e62f014a4bf8d6a8e8f0f5e1162dea77dfc4da0c7
```

**Note**: 1st param = nft manager address, 3rd and 4th = token0(“eth”) and token1(erc20)

### Recap
We should have the following in the local devnet:
- ERC20
- Factory
- NFT Manager (used for calling mints, burns, collects)
- Swap Manager (used for calling swaps)
- Pool for ETH and ERC20

## Run the Python Script
Now, the devnet setup is complete. We may start executing the desired transactions on it.

For this, we will use [main.py](main.py)

First you should set up the appropriate addressess at the beggining of the file

This program will then create a client to interact on both mainnet and devnet. It will then get all the events emitted by the desired contract on mainnet, and get the transaction info related to them. It will then create a copy of the calls executed within those transactions, storing the information needed to replicate this calls on devnet (Contract address called, Selector called, Calldata sent).

Finally it will send all these transactions on the local devnet, achieving a local copy of the final state of the pool.
