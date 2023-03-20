
# CODE FOR PAYMENT TRXN BY CREATING THE ACCOUNT USING FUNCTION


import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk import transaction

# first call the generate_algorand_keypair()
# then node down address, private key, and the passphrase for later usage
# Then fund this address
# then comment in the call for generate_algorand_keypair()
# Finally pass the address and private key while calling the function first_transaction_example(private_key, my_address)

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
#
# My address: OQ35AQMGOYIDB2UIUY4RXHCQPSDVY7WNDSL7LC4ILP7SO7KBJ46FR6LJ5Y
# My private key: A5efY/ULU8gpqnfDsTQ17sjcTItKxoI0ayoOIIWkazZ0N9BBhnYQMOqIpjkbnFB8h1x+zRyX9YuIW/8nfUFPPA==
# My passphrase: there layer range satisfy plastic improve eyebrow jeans debris spot box moment ridge spring february shock motion proud benefit abstract apart truck rebuild ability define

# Write down the address, private key, and the passphrase for later usage
generate_algorand_keypair()

def first_transaction_example(private_key, my_address):
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "gqXFTgP7M54pqYRdPxIm14LBaRGynGMO4BodJRoc"
    headers = {
        "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    receiver = "PIDOSB3YFVJPHYNBMMKFMWWYWJ3BW62V2NX3O6SXI5WOG2KJPYFDIVV4AE"
    amount = 100000
    note = "Hello Bob. This is my first transaction".encode()

    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )
    print("Fee: {} microAlgos".format(params.fee) )

    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")


# replace private_key and my_address with your private key and your address.
first_transaction_example('A5efY/ULU8gpqnfDsTQ17sjcTItKxoI0ayoOIIWkazZ0N9BBhnYQMOqIpjkbnFB8h1x+zRyX9YuIW/8nfUFPPA==', 'OQ35AQMGOYIDB2UIUY4RXHCQPSDVY7WNDSL7LC4ILP7SO7KBJ46FR6LJ5Y')
