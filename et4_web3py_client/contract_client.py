import json
import binascii

from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.contract import ConciseContract, ImplicitContract

from web3.middleware import geth_poa_middleware
from web3.middleware import time_based_cache_middleware, simple_cache_middleware, latest_block_based_cache_middleware
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.gas_strategies.time_based import fast_gas_price_strategy, medium_gas_price_strategy


NODE = 'http://127.0.0.1:48545'
CONTRACT = Web3.toChecksumAddress('0x308476d2b237e38dd9ba297c4dda8e62aa20f52f')
OWNER = Web3.toChecksumAddress('0x6412fcedcedeb20a8bb990c6041d2cdee0404fa7')
RECIPIENT = Web3.toChecksumAddress('0xff989e7d397e6ff1026429a87d7a5ef7c6b09c27')
FEE_RECIPIENT = Web3.toChecksumAddress('0x8862ce71fdcdc386d5a9b6bb5640a8fefd6ddad0')

COMPILED_CONTRACT = './ET4Token.json'


def init_contract(node_address=NODE, contract_address=CONTRACT, contract_data=COMPILED_CONTRACT, is_poa=True):
    web3_inst = Web3(HTTPProvider(node_address))

    web3_inst.eth.setGasPriceStrategy(rpc_gas_price_strategy)
    # web3_inst.eth.setGasPriceStrategy(fast_gas_price_strategy)
    # web3_inst.eth.setGasPriceStrategy(medium_gas_price_strategy)

    web3_inst.middleware_stack.add(simple_cache_middleware)
    web3_inst.middleware_stack.add(latest_block_based_cache_middleware)
    web3_inst.middleware_stack.add(time_based_cache_middleware)

    if is_poa:
        web3_inst.middleware_stack.inject(geth_poa_middleware, layer=0)

    with open(contract_data, 'r') as contract_definition:
        contract_json = json.load(contract_definition)
    contract_obj = web3_inst.eth.contract(
        address=contract_address,
        abi=contract_json['abi']
    )

    return contract_obj, web3_inst


def mint(inst, addr, amount, tx_p=None):
    tx_hash = inst.mint(addr, amount, transact=tx_p)
    print(f'waiting for tx {binascii.hexlify(tx_hash)}')
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt


def start_escrow(inst, escrow_id, recipient, amount, tx_p=None):
    tx_hash = inst.startEscrow(Web3.toBytes(escrow_id), recipient, amount, transact=tx_p)
    print(f'waiting for tx {binascii.hexlify(tx_hash)}')
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt


def release_escrow(inst, escrow_id, fee_recipient, tx_p=None):
    tx_hash = inst.releaseEscrow(Web3.toBytes(escrow_id), fee_recipient, transact=tx_p)
    print(f'waiting for tx {binascii.hexlify(tx_hash)}')
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt


def cancel_escrow(inst, escrow_id, tx_p=None):
    tx_hash = inst.cancelEscrow(Web3.toBytes(escrow_id), transact=tx_p)
    print(f'waiting for tx {binascii.hexlify(tx_hash)}')
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt


if __name__ == '__main__':
    contract, web3 = init_contract()
    print(web3.eth.syncing)

    generated_price = web3.eth.generateGasPrice()

    c_contract = ConciseContract(contract)
    t_contract = ImplicitContract(contract)

    print('Network gas price:', web3.fromWei(web3.eth.gasPrice, 'Gwei'))
    print('Computed gas price:', web3.fromWei(generated_price, 'Gwei'))
    # print(web3.eth.accounts)
    # print(web3.txpool.content)
    params = {
        'from': OWNER,
        'gasPrice': generated_price
    }

    # mint(t_contract, web3.eth.accounts[0], web3.toWei(1, 'Ether'), tx_p=params)
    # mint(t_contract, '0x8862cE71FDCDC386D5a9b6BB5640a8FefD6DDAd0', web3.toWei(100000, 'Ether'), tx_p=params)
    # mint(t_contract, '0xfF989e7D397e6fF1026429A87d7A5eF7c6B09c27', web3.toWei(100000, 'Ether'), tx_p=params)

    print('OWNER', c_contract.balanceOf(OWNER))
    print('RECIPIENT', c_contract.balanceOf(RECIPIENT))
    print('FEE_RECIPIENT', c_contract.balanceOf(FEE_RECIPIENT))

    print('starting transaction...')
    receipt = start_escrow(t_contract, 1122334455, RECIPIENT, web3.toWei(50, 'Gwei'), tx_p=params)
    print(receipt)
    print('releasing transaction...')
    receipt = release_escrow(t_contract, 1122334455, FEE_RECIPIENT, tx_p=params)
    print(receipt)

    print('OWNER', c_contract.balanceOf(OWNER))
    print('RECIPIENT', c_contract.balanceOf(RECIPIENT))
    print('FEE_RECIPIENT', c_contract.balanceOf(FEE_RECIPIENT))

    print('starting transaction...')
    receipt = start_escrow(t_contract, 1122334455, RECIPIENT, web3.toWei(50, 'Gwei'), tx_p=params)
    print(receipt)
    print('cancelling transaction...')
    receipt = cancel_escrow(t_contract, 1122334455, tx_p=params)
    print(receipt)

    print('OWNER', c_contract.balanceOf(OWNER))
    print('RECIPIENT', c_contract.balanceOf(RECIPIENT))
    print('FEE_RECIPIENT', c_contract.balanceOf(FEE_RECIPIENT))
