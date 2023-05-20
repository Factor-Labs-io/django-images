from web3 import Web3
import json

import os
from dotenv import load_dotenv

load_dotenv()  

infura_project_id = os.environ.get("INFURA_PROJECT_ID")  

CONTRACT_ADDRESS = "0xdf8bFB139AD21Ec238B9e56BeD6f0953202cF104"

w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{infura_project_id}"))

with open("strangershq/contract_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def getWalletBalance(address):
    balance = contract.functions.balanceOf(address).call()
    return balance

def getTokens(address):
    balance = getWalletBalance(address)
    token_ids = []
    for i in range(0, balance):
        try:
            token = contract.functions.boardedTokenId(address, i).call()
            token_ids.append(token)
        except:
            pass
    return token_ids

def getOnChainPoints(address):
    token_ids = getTokens(address)
    points = 0
    for token in token_ids:
        points += contract.functions.checkActiveBoardingPoints(token).call()
    points += contract.functions.boarderAcc(address).call()
    return points
