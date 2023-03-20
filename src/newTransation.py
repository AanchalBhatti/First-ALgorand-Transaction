# CODE FOR PAYMENT TRXN BY using the information of THE ACCOUNT already created using USER INTERFACE

import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk import transaction

def first_transaction_example(private_key, my_address):
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "gqXFTgP7M54pqYRdPxIm14LBaRGynGMO4BodJRoc"
    headers = {
        "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    # algod_token = "gqXFTgP7M54pqYRdPxIm14LBaRGynGMO4BodJRoc"
    # algod_client = algod.AlgodClient(algod_token, algod_address)

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


my_address ='2T7INOB2KC3IQVPVE6ERXVBI7ID2YLUIKLYOT4L2ZESPMPT3LE2DIXPJJA'
private_key =mnemonic.to_private_key('able athlete cradle suspect manage entry fat glimpse riot gap ladder behave fuel rescue inherit happy salon current ocean decade thought prison hero ability anxiety')
# replace private_key and my_address with your private key and your address.
first_transaction_example(private_key, my_address)
